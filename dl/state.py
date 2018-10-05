from collections import defaultdict
from torchnet import meter
from prometheus.utils.factory import UtilsFactory
from prometheus.utils.misc import FrozenClass


class RunnerState(FrozenClass):
    """
    An object that is used to pass internal state during train/valid/infer.
    """

    def __init__(self, **kwargs):
        # special info
        self.device = None
        self.loader_mode = None
        self.reset_step = kwargs.get("reset_step", False)

        # data pipeline
        self.input = None
        self.output = None

        # counters
        self.loader_len = 0
        self.batch_size = 0
        self.step = 0
        self.epoch = 0

        # metrics
        self.lr = defaultdict(lambda: 0)
        self.momentum = defaultdict(lambda: 0)
        self.loss = defaultdict(lambda: 0)

        self.batch_metrics = defaultdict(lambda: 0)
        self.epoch_metrics = defaultdict(
            lambda: defaultdict(lambda: meter.AverageValueMeter()))
        self.valid_metrics = None
        self.best_metrics = None

        # other
        self.is_train = False
        for k, v in kwargs.items():
            setattr(self, k, v)

        self._freeze()

    @staticmethod
    def on_stage_init_pre(model, stage):
        pass

    @staticmethod
    def on_stage_init_post(model, stage):
        pass

    @staticmethod
    def on_train_start_pre(state):
        pass

    @staticmethod
    def on_train_start_post(state):
        pass

    @staticmethod
    def on_train_end_pre(state):
        pass

    @staticmethod
    def on_train_end_post(state):
        pass

    @staticmethod
    def on_infer_start_pre(state):
        pass

    @staticmethod
    def on_infer_start_post(state):
        pass

    @staticmethod
    def on_infer_end_pre(state):
        pass

    @staticmethod
    def on_infer_end_post(state):
        pass

    @staticmethod
    def on_epoch_start_pre(state):
        pass

    @staticmethod
    def on_epoch_start_post(state):
        pass

    @staticmethod
    def on_epoch_end_pre(state):
        pass

    @staticmethod
    def on_epoch_end_post(state):
        state.epoch_metrics = defaultdict(
            lambda: defaultdict(lambda: meter.AverageValueMeter()))

    @staticmethod
    def on_loader_start_pre(state):
        pass

    @staticmethod
    def on_loader_start_post(state):
        pass

    @staticmethod
    def on_loader_end_pre(state):
        lm = state.loader_mode
        state.epoch_metrics[lm] = {
            key: UtilsFactory.get_val_from_metric(value)
            for key, value in state.epoch_metrics[lm].items()
        }

    @staticmethod
    def on_loader_end_post(state):
        if state.reset_step:
            state.step = None

    @staticmethod
    def on_batch_start_pre(state):
        state.batch_metrics = defaultdict(lambda: 0)

    @staticmethod
    def on_batch_start_post(state):
        pass

    @staticmethod
    def on_batch_end_pre(state):
        pass

    @staticmethod
    def on_batch_end_post(state):
        lm = state.loader_mode
        for key, value in state.batch_metrics.items():
            state.epoch_metrics[lm][key].add(value)
        state.step += state.batch_size
