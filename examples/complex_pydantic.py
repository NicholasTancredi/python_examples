from enum import Enum
from typing import NamedTuple, Optional

import arrow
from pydantic import BaseModel, PydanticValueError
from pytypes import typechecked


class KindEnum(Enum):
    POSEJOB = 'POSEJOB'


@typechecked
class BlobInfoObject(NamedTuple):
    name: str
    bucket: str = 'pc.BUCKET_NAME'


class PoseJobIdKeyError(PydanticValueError):
    code = 'PoseJobIdKeyError'
    msg_template = '"id" is required when "outputBlobInfoVideo" is not provided.'


class PoseJob(BaseModel):
    # DEFAULTS
    modelVersion: str = '2.0.2'
    kind: KindEnum = KindEnum.POSEJOB
    createdAt: str = arrow.utcnow().format()
    updatedAt: str = arrow.utcnow().format()

    # OPTIONAL
    id: Optional[int] = None
    outputBlobInfoVideo: Optional[BlobInfoObject] = None
    outputBlobInfoPoseData: Optional[BlobInfoObject] = None
    userIP: Optional[str] = None
    userHostname: Optional[str] = None

    def __init__(self, **kwargs):
        _kwargs = kwargs

        # NOTE: Prevents _kwargs['id'] from throwing KeyError is 'id' is not provided, 
        # alternatively you could check for it like `if 'id' not in _kwargs`, 
        # the edge case makes this ugly either way, but at least here its 
        # typechecked before it gets to outputBlobInfoVideo
        super().__init__(**_kwargs)

        if 'outputBlobInfoVideo' not in _kwargs:
            #  Probably shouldn't even have this happen, but I'm assuming other things would need to be restructured...
            if _kwargs['id'] is None:
                raise PoseJobIdKeyError()

            _kwargs['outputBlobInfoPoseData'] = BlobInfoObject(
                name='{}/video.mp4'.format(_kwargs['id'])
            )

        if 'outputBlobInfoPoseData' not in _kwargs:
            if _kwargs['id'] is None:
                raise PoseJobIdKeyError()

            _kwargs['outputBlobInfoPoseData'] = BlobInfoObject(
                name='{}/data.json'.format(_kwargs['id'])
            )

        super().__init__(**_kwargs)
