from oauth2.adapters.common.setting import SettingBase


class Setting(SettingBase):

    class Config:
        env_prefix = 'VK_'
