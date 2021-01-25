from tests import client


def test_x12_post(x12_270_basic_message: str):
    response = client.post('/x12', json={'x12': x12_270_basic_message})
    assert response.status_code == 200

    json_response = response.json()

    x12_271_message = 'ISA*00*          *00*          *ZZ*890069730      *ZZ*154663145      *200929*1705*|*00501*000000001*0*T*:~GS*HS*890069730*154663145*20200929*1705*0001*X*005010X279A1~ST*271*4321*005010X279A1~BHT*0022*11*10001234*20060501*1319~HL*1**20*1~NM1*PR*2*ABC COMPANY*****PI*842610001~HL*2*1*21*1~NM1*1P*2*BONE AND JOINT CLINIC*****SV*2000035~HL*3*2*22*0~TRN*2*1453915417*9877281234~NM1*IL*1*DOE*JOHN****MI*11122333301~DMG*D8*19800519*~DTP*346*D8*20060101~EB*1**30**GOLD 123 PLAN~EB*L~EB*1**1>33>35>47>86>88>98>AL>MH>UC~EB*B**1>33>35>47>86>88>98>AL>MH>UC*HM*GOLD 123 PLAN*27*10*****Y~EB*B**1>33>35>47>86>88>98>AL>MH>UC*HM*GOLD 123 PLAN*27*30*****N~LS*2120~NM1*P3*1*JONES*MARCUS****SV*0202034~LE*2120~SE*20*4321~'
    assert json_response['x12'] == x12_271_message
    assert json_response['x12_transaction_code'] == '271'
