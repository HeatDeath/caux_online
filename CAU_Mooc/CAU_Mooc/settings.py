import os
import sys
import pymysql


pymysql.install_as_MySQLdb()
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 设置 apps 目录
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))
sys.path.insert(0, os.path.join(BASE_DIR, 'extra_apps'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '_#c&3xf-v&yub6_!@e*18_yhd44o=@+yuv48t1!^6qd8lhnmwc'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# 重载 AUTHENTICATION_BACKENDS
AUTHENTICATION_BACKENDS = (
    'user_member.views.CustomBackend',
)


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 注册 Apps
    'user_member',
    'mooc_course',
    'cau_college',
    'user_operation',
    'site_manage',
    # 注册 xadmin 后台管理工具
    'xadmin',
    'crispy_forms',
    # 注册 captcha 随机验证码生成工具
    'captcha',
    # 注册 pure_pagination 分页工具
    'pure_pagination',
]

# 使用重新设计的 PersonalInformation 表替换 auth 的 User 表
AUTH_USER_MODEL = 'user_member.PersonalInformation'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'CAU_Mooc.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # 把 MEDIA_URL 注册到 html 文件中 ，这样在 html 中就可以用 MEDIA_URL 变量
                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'CAU_Mooc.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'caux_online',
        'USER': 'root',
        'PASSWORD': 'roottest',
        'HOST': '127.0.0.1',
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# 邮件服务器
EMAIL_HOST = 'smtp.sina.com'
# 邮件服务器端口
EMAIL_PORT = 25
# 邮件服务器用户
EMAIL_HOST_USER = 'mydjangotest@sina.com'
# 邮件服务器密码
EMAIL_HOST_PASSWORD = 'django666666'
EMAIL_USE_TLS = False
# 邮件发送者
EMAIL_FROM = 'mydjangotest@sina.com'
