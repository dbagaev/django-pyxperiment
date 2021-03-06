from .models import models

from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404

from pyxperiment.experiment import Experiment, Registry


def reload_cases(test, mdl_test):

    experiments_found  = test.findExperiments()

    for mdl_case in models.Experiment.objects.filter(ExperimentSet=mdl_test):
        case_found = False
        for case in experiments_found:
            if case.Name == mdl_case.Name:
                case_found = True
                break

        if not case_found:
            mdl_case.delete()

    for case in experiments_found:
        mdl_case = models.Experiment.objects.filter(Name=case.Name, ExperimentSet=mdl_test)
        if len(mdl_case) == 0:
            mdl_case = models.Experiment(Name=case.Name, ExperimentSet=mdl_test)
            mdl_case.save()


def reload_metrics(test, mdl_test):
    for metric in test.AllMetrics():
        mdl_metric = models.Metric.objects.filter(Name=metric[0], ExperimentSet=mdl_test)
        if len(mdl_metric) == 0:
            mdl_metric = models.Metric(
                    Name=metric[0],
                    ExperimentSet=mdl_test )
        else :
            mdl_metric = mdl_metric[0]

        mdl_metric.Type = metric[1].Type
        mdl_metric.Accumulator = (metric[1]._Accumulator is not None)
        mdl_metric.save()




def reload(request):
    all_experiment_sets = Registry.getInstance()._ExperimentSets.values()

    for mdl_test in models.ExperimentSet.objects.all():
        test_registered = False
        for test in all_experiment_sets:
            if test.Name == mdl_test.Type:
                test_registered = True
                break

        if not test_registered:
            mdl_test.delete()

    for test in all_experiment_sets:
        mdl_test = models.ExperimentSet.objects.filter(Type=test.Name)
        if len(mdl_test) == 0:
            mdl_test = models.ExperimentSet(Type=test.Name)
            mdl_test.save()
        else:
            mdl_test = mdl_test[0]

        reload_cases(test, mdl_test)
        reload_metrics(test, mdl_test)

    return redirect('django-pyxperiment:index')
