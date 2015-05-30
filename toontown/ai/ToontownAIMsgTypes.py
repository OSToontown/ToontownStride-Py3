from otp.ai.AIMsgTypes import *
TTAIMsgName2Id = {'DBSERVER_GET_ESTATE': 1040,
 'DBSERVER_GET_ESTATE_RESP': 1041,
 'PARTY_MANAGER_UD_TO_ALL_AI': 1042}
TTAIMsgId2Names = invertDictLossless(TTAIMsgName2Id)
globals().update(TTAIMsgName2Id)

DBSERVER_PET_OBJECT_TYPE = 5
