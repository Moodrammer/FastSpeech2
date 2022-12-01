import torch
import yaml

from inference import infer_tts, prepare_tts_model
from utils.utils import load_file_to_data, predict

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")


class TextToSpeech:
    def __init__(
        self,
        prepare_tts_model_path,
        model_config_path,
        train_config_path,
        vocoder_config_path=None,
        speaker_pre_trained_path=None,
        root_path=None,
        Model_URL=None,
    ):
        self.prepare_tts_model = yaml.load(open(prepare_tts_model_path, "r"), Loader=yaml.FullLoader)
        # TODO: fix this trick
        if self.prepare_tts_model["path"]["stats_path"][0] != "/":
            self.prepare_tts_model["path"]["stats_path"] = f"{root_path}/{self.prepare_tts_model['path']['stats_path']}"
        if self.prepare_tts_model["path"]["lexicon_path"][0] != "/":
            self.prepare_tts_model["path"][
                "lexicon_path"
            ] = f"{root_path}/{self.prepare_tts_model['path']['lexicon_path']}"
        self.model_config = yaml.load(open(model_config_path, "r"), Loader=yaml.FullLoader)
        self.train_config = yaml.load(open(train_config_path, "r"), Loader=yaml.FullLoader)
        self.configs = (self.prepare_tts_model, self.model_config, self.train_config)
        self.vocoder_config_path = vocoder_config_path
        self.speaker_pre_trained_path = speaker_pre_trained_path
        self.model, self.vocoder, self.configs = prepare_tts_model(
            self.configs, self.vocoder_config_path, self.speaker_pre_trained_path,Model_URL
        )

    def synthesize(self, text, bw=False, apply_tshkeel=False, controls=(1.0, 1.0, 1.0)):
        p_control, e_control, d_control = controls
        infer_tts(text, self.model, self.vocoder, self.configs, bw=bw, apply_tshkeel=apply_tshkeel, pitch_control=p_control, energy_control=e_control, duration_control=d_control)
