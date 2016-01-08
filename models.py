from django.db import models

from pyxperiment.metric import Metric as exp_Metric

# Create your models here.
class ExperimentSet(models.Model):
    Type = models.CharField(max_length=128)

    def Experiments(self):
        return Experiment.objects.filter(ExperimentSet=self)

    def Metrics(self):
        return Metric.objects.filter(ExperimentSet=self)


class Experiment(models.Model):
    Name = models.CharField(max_length=256)
    ExperimentSet = models.ForeignKey('ExperimentSet', on_delete=models.CASCADE)

    def Metrics(self):
        return Metric.objects.filter(Experiment=self)


class Run(models.Model):
    Started = models.TimeField(auto_now=True)


class ExperimentRun(models.Model):
    Started = models.TimeField(auto_now=True)
    Success = models.IntegerField()
    Run = models.ForeignKey('Run', on_delete=models.CASCADE)
    Experiment = models.ForeignKey('Experiment', on_delete=models.CASCADE)


class Metric(models.Model):
    VALUE_TYPES = (
        (exp_Metric.TYPE_FLOAT, 'Float'),
        (exp_Metric.TYPE_INTEGER, 'Integer'),
        (exp_Metric.TYPE_BOOLEAN, 'Boolean'),
        (exp_Metric.TYPE_STRING, 'String'),
        (exp_Metric.TYPE_FILE, 'File')
    )

    Name = models.CharField(max_length=64)
    Type = models.IntegerField(choices=VALUE_TYPES)

    ExperimentSet = models.ForeignKey('ExperimentSet', on_delete=models.CASCADE)

class MetricValue(models.Model):
    ExperimentRun = models.ForeignKey('ExperimentRun', on_delete=models.CASCADE, db_constraint=False, null=True)
    Run = models.ForeignKey('Run', on_delete=models.CASCADE)
    Metric = models.ForeignKey('Metric', on_delete=models.CASCADE)

    @property
    def StrValue(self) :
        if self.Metric.Type == exp_Metric.TYPE_FLOAT :
            v = MetricFloatValue.objects.filter(MetricValue=self)
            if len(v) == 0 :
                return ""
            else :
                return str(v[0].Value)
        elif self.Metric.Type == exp_Metric.TYPE_INTEGER :
            v = MetricIntegerValue.objects.filter(MetricValue=self)
            if len(v) == 0 :
                return ""
            else :
                return str(v[0].Value)
        elif self.Metric.Type == exp_Metric.TYPE_STRING :
            v = MetricStringValue.objects.filter(MetricValue=self)
            if len(v) == 0 :
                return ""
            else :
                return str(v[0].Value)
        elif self.Metric.Type == exp_Metric.TYPE_BOOLEAN :
            v = MetricBooleanValue.objects.filter(MetricValue=self)
            if len(v) == 0 :
                return ""
            else :
                return str(v[0].Value)

        else :
            return ""


class MetricStringValue(models.Model):
    MetricValue = models.ForeignKey('MetricValue', on_delete=models.CASCADE)
    Value = models.CharField(max_length=256)


class MetricFloatValue(models.Model):
    MetricValue = models.ForeignKey('MetricValue', on_delete=models.CASCADE)
    Value = models.FloatField()


class MetricIntegerValue(models.Model):
    MetricValue = models.ForeignKey('MetricValue', on_delete=models.CASCADE)
    Value = models.IntegerField()


class MetricFileValue(models.Model):
    MetricValue = models.ForeignKey('MetricValue', on_delete=models.CASCADE)


class MetricBooleanValue(models.Model):
    MetricValue = models.ForeignKey('MetricValue', on_delete=models.CASCADE)
    Value = models.BooleanField()
