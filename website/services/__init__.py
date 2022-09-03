from services.web.core.logger import log
from services.web.website.services.cache_service import CacheService
from services.web.website.services.login_service import LoginService
from services.web.website.services.mail_service import MailService
from services.web.website.services.redis_service import RedisService
from services.web.website.config import GlobalConfig

cache_service = CacheService()
mail_service = MailService()
login_service = LoginService()
redis_service = RedisService()


def init_services(app):
    cache_service.init_cache(app)
    log("Cache Service Inited", 4)
    mail_service.init_mail(app)
    log("Mail Service Inited", 4)
    login_service.init_login(app)
    log("Login Service Inited", 4)
    login_service.session_protection = "strong"
    if GlobalConfig.docker:
        redis_service.init(host="localhost", port=6379)
        log("Redis Service Inited", 4)
