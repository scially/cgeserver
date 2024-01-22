from typing import Optional, Dict, List
import uuid
import subprocess
import logging
from pathlib import Path
from sqlmodel import SQLModel, Field
from pydantic.fields import PrivateAttr

logger = logging.getLogger(__name__)

class SSRModel(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    uid: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4)
    name: str
    background: Optional[bool] = True
    uepath: Optional[str] = None
    frontpath: Optional[str] = None
    status: bool = False
    xresolution: int = 1920
    yresolution: int = 1080
    
    _process: subprocess.Popen = PrivateAttr(None)
    
    def run(self) -> bool:
        if Path(self.uepath).exists() and not self.status:
            cmds = [self.uepath,
                    "-AudioMixer", 
                    "-NoTextureStreaming", 
                    "-binnedmalloc3", 
                    "-AllowPixelStreamingCommands", 
                    f"-PixelStreamingURL=ws://127.0.0.1:{PORT}/client/{self.uid}", 
                    f"-ws=ws://127.0.0.1:{PORT}/message/{self.uid}"]
            if self.background:
                cmds = cmds + ["-RenderOffScreen", "-ForceRes"]
            
            cmds = cmds + [f"-ResX={self.xresolution}", f"-Resy={self.xresolution}"]
            cmds = cmds + ["-NvEncH264ConfigLevel=NV_ENC_LEVEL_H264_52"]
            self._process = subprocess.Popen(cmds)
            logger.info("[Render] Render Start: %s", ' '.join(cmds))
            return True
        
        return False

    def stop(self) -> None:
        if self._process is not None:
            self._process.kill()