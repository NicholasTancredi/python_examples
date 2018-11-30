from enum import Enum
# from pydantic import BaseModel
# from typing import NamedTuple
from pytypes import typechecked
import arrow

# import project_constants as pc
# from src.pose_platform_constants.status import StatusEnum, StatusTypes
# from src.pose_platform_constants.assessments import AssessmentEnum

class KindEnum(Enum):
    pose_job = 'pose_job'


@typechecked
class BlobInfoObject(NamedTuple):
    name: str
    bucket: str = 'pc.BUCKET_NAME'


from pydantic import BaseModel, PydanticValueError
from typing import NamedTuple, Optional
# ...
class PoseJobIdKeyError(PydanticValueError):
    code = 'PoseJobIdKeyError'
    msg_template = '"id" is required when "outputBlobInfoVideo" is not provided.'


class PoseJob(BaseModel):
    # REQUIRED
    # assessment: AssessmentEnum
    # inputBlobInfo: BlobInfoObject

    # DEFAULTS
    modelVersion: str = '2.0.2'
    # status: StatusEnum = StatusEnum.INITIALIZING
    # kind: KindEnum = KindEnum.pose_job
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

        # NOTE: Default bucket can be set on BlobInfoObject
        # defaultBucket = pc.BUCKET_NAME
        # ...
        # @typechecked
        # class BlobInfoObject(NamedTuple):
        #     name: str
        #     bucket: str = pc.BUCKET_NAME
        if 'outputBlobInfoVideo' not in _kwargs:
            #  Probably shouldn't even have this happen, but I'm assuming other things would need to be restructured...
            if _kwargs['id'] is None:
                raise PoseJobIdKeyError()

            # These would throw an error `value is not a valid tuple (type=type_error.tuple)`
            # _kwargs['outputBlobInfoVideo'] = {
            #     'name': '{}/video.mp4'.format(_kwargs['id']),
            #     'bucket': defaultBucket
            # }

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


class Test(BaseModel):
    a: str = 'a'


Test()