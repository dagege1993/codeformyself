# coding: utf8
"""Actions for aliyun ecs.

Such as create boot and destroy.
Powered by celery.
"""

import base64
from enum import Enum
from typing import Dict

from aliyunsdkcore.client import AcsClient
from aliyunsdkecs.request.v20140526 import StartInstanceRequest
from aliyunsdkecs.request.v20140526 import CreateInstanceRequest
from aliyunsdkecs.request.v20140526 import DeleteInstanceRequest
from aliyunsdkcore.acs_exception.exceptions import ServerException

from tasks import settings
from tasks.application import app
from tasks.utils.database import databases

alisdk = AcsClient(
    settings.ALIYUN_ACCESS_KEY_ID,
    settings.ALIYUN_ACCESS_KEY_SECRET,
    'cn-beijing'
)

userdata = b'''#include
http://scripture-html.oss-cn-beijing.aliyuncs.com/scripts/scripts/base.cloud-init
http://scripture-html.oss-cn-beijing.aliyuncs.com/scripts/scripts/conda.cloud-init
'''


class InternetChargeType(Enum):
    """Internet charge type."""

    PayByTraffic = 'PayByTraffic'
    PayByBandwidth = 'PayByBandwidth'


ICT = InternetChargeType


@app.task
def create_from_template(template):
    """Create ecs instance by template."""
    db = databases.get('scripture')
    tmpl = db.op_vm_templates.find_one({'name': template})
    return create(**tmpl)


@app.task
def create(*, instance_name: str, instance_type: str, image_id: str, sgid: str,
           internet_charge_type: ICT = InternetChargeType.PayByTraffic,
           host_name: str = '', password: str = '', key_pair_name: str = '',
           userdata: bytes = b'', vswitch_id: str = '') -> Dict:
    """Create new ecs instance.

    params:
        instance_type
    """
    request = CreateInstanceRequest.CreateInstanceRequest()
    request.set_ImageId(image_id)
    request.set_InstanceType(instance_type)
    request.set_SecurityGroupId(sgid)
    request.set_InstanceName(instance_name)
    request.set_InternetChargeType(internet_charge_type)
    if not host_name:
        host_name = instance_name
    request.set_HostName(host_name)  # Optional
    if password:
        request.set_Password(password)  # Optional
    if key_pair_name:
        request.set_KeyPairName(key_pair_name)

    if userdata:
        base64_bytes = base64.encodebytes(userdata)
        request.set_UserData(base64_bytes)

    if vswitch_id:
        request.set_VSwitchId(vswitch_id)

    return alisdk.do_action_with_exception(request)


@app.task
def boot(*, instance_id: str) -> Dict:
    """Let ecs instance of id start up.

    Params:
        instance_id: Id of ecs instance, must be poweroff.

    Returns: response info

    """
    request = StartInstanceRequest.StartInstanceRequest()
    request.set_InstanceId(instance_id)

    return alisdk.do_action_with_exception(request)


@app.task
def destroy(*, instance_id: str) -> bool:
    """Destroy an ecs instance by instance id.

    Params:
        instance_id: Id of ecs instance, must be poweroff.

    Returns: Bool

    """
    request = DeleteInstanceRequest.DeleteInstanceRequest()
    request.set_InstanceId(instance_id)
    try:
        response = alisdk.do_action_with_exception(request)

    except ServerException:
        pass

    return response


@app.task
def deploy():
    """Deploy scripture to new ecs.

    Returns:
        bool: True if success, False otherwise

    """
    pass
