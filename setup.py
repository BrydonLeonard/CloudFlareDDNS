from setuptools import setup

setup(name='cloudflare_ddns',
      version='0.1',
      description='Simple script to make CloudFlare DNS dynamic!',
      url='https://github.com/BrydonLeonard/CloudFlareDDNS',
      author='Brydon Leonard',
      author_email='brydon.leonard@gmail.com',
      license='MIT',
      packages=['cloudflare_ddns'],
      zip_safe=False,
      install_requires=['requests'])