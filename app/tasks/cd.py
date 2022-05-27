import os
import subprocess
import traceback

from celery.utils.log import get_task_logger

from app.services import celery

logger = get_task_logger(__name__)


@celery.task
def continuous_development():
    try:
        if subprocess.check_output('git branch --show-current'.split(), text=True).strip() == 'production':
            for command in ['git checkout master', 'git pull origin master', 'git branch -D production', 'git fetch origin production',
                            'git checkout production', 'echo thatswhatshesaid | sudo -S systemctl restart nginx && sudo -S supervisorctl reload']:
                subprocess.run(command, check=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True,
                               preexec_fn=os.setsid)
    except Exception as e:
        logger.critical(f"{str(e)} \n {traceback.format_exc()}\n\n")
        return False
