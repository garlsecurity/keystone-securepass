from setuptools import setup, find_packages

setup(
    name='keystone-securepass',
    version='1.0',

    description='SecurePass Keystone driver for OpenStack',

    author='Giuseppe Paterno',
    author_email='gpaterno@garl.ch', 

    url='https://github.com/garlsecurity/keystone-securepass',

    classifiers=[
                 'License :: OSI Approved :: Apache Software License',
                 'Programming Language :: Python',
                 'Programming Language :: Python :: 2',
                 'Programming Language :: Python :: 2.7',
                 'Programming Language :: Python :: 3',
                 'Programming Language :: Python :: 3.4',
                 ],

    platforms=['Any'],

    scripts=[],

    provides=[
		'keystone-securepass',
              ],

    packages=find_packages(),
    include_package_data=True,

    entry_points={
        'keystone.identity': [
            'securepass = keystone.identity.backends.securepass:Identity',
        ],
    },

    zip_safe=False,
)

