import os
import re
import sys
from atmisc import atlogger, atgen, spinner

class LabAccount():
    ''' Lab Account credentials encoding

    This class will decode hidden lab account for use by Unlocking. If metadata is missing, then script will
    use given username and password.
    '''

    __metadata = """
    KFxTKyk6IChcUysp
    dXNlcm5hbWU6ICBwbGF0c2lfdGVzdA==
    VVNFUk5BTUU6IHNpbGljb25fZ3JvdXA=
    dXNlcm5hbWU6IHRlc3RfcGxhdHNpIA==
    dXNlcm5hbWU6ICBzaWxpY29uX2dyb3Vw
    cGFzc3dvcmQ6IENsMWVudC1FbDNjdHJpY2Fs
    UEFTU1dPUkQ6IENMSUVOVEdST1VQICAgICA=
    UEFTU1dPUkQ6ICBFbGVjdHJpY2FsX1NvbWU=
    cGFzc3dvcmQ6ICBQbGF0c2lBY2Nlc3MgICA=
    """

    def __init__(self):
        ''' 
		If metadata is included, will continue to gather metadata. Otherwise do nothing.
        '''
        if(self.__metadata):
            self.__gather_metadata()
            self._retrieved = bool(self.__values['username']) and bool(self.__values['password'])
        else:
            self._retrieved = False

    @property
    def retrieved(self):
        ''' (bool): True if we retrieved correct username and password. False otherwise.
        '''
        return self._retrieved

    @property
    def username(self):
        ''' (str): Username of Lab Account (if retrieved)
        '''
        return self.__values['username']

    @property
    def password(self):
        ''' (str): Password of Lab Account (if retrieved)
        '''
        return self.__values['password']

    def __gather_metadata(self):
        import base64

        self.__values = atgen.ViviDict()
        m_patt = re.compile(base64.b64decode(self.__metadata.split("\n")[1]).decode("utf-8"))
        for line in self.__metadata.split("\n"):
            translation = base64.b64decode(line).decode("utf-8")
            if(translation and m_patt.search(translation)):
                reference, value = m_patt.findall(translation)[0]
                if(reference == 'username' or reference == 'password'):
                    self.__values[reference] = value

if __name__ == "__main__":
    lab_account = LabAccount()
    print(lab_account.username, lab_account.password)