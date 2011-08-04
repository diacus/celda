# -*- coding:utf-8 -*-

"""
File: ida.py
Author: diacus
Description: IDA interface
"""

import logging, os, shlex, subprocess
from data.stream import BlockStream, FragmentStream
from lib.common  import MessagesENG as Messages
from lib.config  import SADConfig

def disperse(fragment):
    """
    Disperse the FragmentStream instance.
    @param fragment: FragmentStream instnace
    @return list instance: contains the generated BlockStreams
    """
    conf     = SADConfig()
    dis      = conf.getdispath()
    cache    = conf.getstoragepath()
    bname    = "%s-%05d.frag" % (fragment.getfilename(),fragment.getpos())
    fragname = os.path.join( cache, bname )
    disp     = [ "%s-%d.ida" % (fragname, k) for k in range(5) ]
    inidis   = Messages.Dispersing % str(fragment)
    enddis   = Messages.Dispersed % str(fragment)
             
    fragment.savetofile(fragname)

    logging.info(inidis)
    subprocess.call([dis, fragname])
    logging.info(enddis)

    blocks = list()

    for k, d in enumerate(disp):
        b = BlockStream(
            os.path.basename(d),
            "IDA",
            fragment.getid(),
            k
        )
        b.loadfromfile(d)
        blocks.append(b)
    
    return blocks

def recover(blockA, blockB, blocC):
    """
    Recovers the original file from the given blocks
    
    @param blockA: BlockStream instance
    @param blockB: BlockStream instance
    @param blockC: BlockStream instance
    
    @return A FragmentStream instance
    """

    conf     = SADConfig()
    rec      = conf.getrecpath()
    cache    = conf.getstoragepath()
    bnames   = list()
    for b in [blockA, blockB, blocC]:
        name = os.path.join( cache, b.getfilename() )
        b.savetofile(name)
        bname.append(name)

    fragname = blockA.getfilename()[:-6]


