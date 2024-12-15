# CHANGELOG


## v1.5.2 (2024-12-15)

### Bug Fixes

- **service_discovery**: A record detection for certain devices
  ([`078f3df`](https://github.com/cbrand/micropython-mdns/commit/078f3df5cb44b4438049a26431ae09aea48b7624))

Ensure that the A record for certain devices (for example shellies) is done correctly by buffering
  currently irrelevant A records as they get sent before the SRV record for the specific target is
  sent.

This change slightly increases memory overhead as an additional configurable buffer needs to be
  added to allow buffering A records which are not yet relevant for an SRV response.

- **service_discovery**: Adjust discover_once to shut down resources
  ([`2331707`](https://github.com/cbrand/micropython-mdns/commit/233170773933aa2de63b10cedbe3daf9392dff15))

If the discover_once method is called and the underyling client and / or discovery has not been
  started by another component ensure to shut down the complete library afterwards to not consume
  any resources without a developer explicitly asking for other functionality in the MDNS library.

### Chores

- Update Makefile
  ([`1503bfa`](https://github.com/cbrand/micropython-mdns/commit/1503bfa0cfed6203b41594c931ca0c0411957790))

fix various configs in the Makefile and add Micropython 1.24 (hacked) support.


## v1.5.1 (2024-12-15)

### Bug Fixes

- Requirements.txt to reduce vulnerabilities
  ([`819b300`](https://github.com/cbrand/micropython-mdns/commit/819b300355cd21bac6092e87fa30051a87f249f2))

The following vulnerabilities are fixed by pinning transitive dependencies: -
  https://snyk.io/vuln/SNYK-PYTHON-ZIPP-7430899

- **Docker**: Fix build files for rp2 versions
  ([`2ed23d4`](https://github.com/cbrand/micropython-mdns/commit/2ed23d457a691656ecab3e4ea824b6cf10cbecba))

copy correct file over with the correct configuration.

- **service_discovery**: Stop discovery loop on stopped client
  ([`5bf8419`](https://github.com/cbrand/micropython-mdns/commit/5bf8419e1b0b5fa59da48198f8b20b6624477520))

The service discovery did not take into account that the client might have shut down in between,
  resulting in a loop running forever reinitializing manually closed clients resulting in
  unexplainable error messages.

### Chores

- **Dockerfile**: Add support for rp2 build for micropython 1.22
  ([`e009cfb`](https://github.com/cbrand/micropython-mdns/commit/e009cfbd276734bd5754b36da8ea8e1e35488974))

- **Dockerfile**: Fix esp32 buidls for 1.21 and 1.22 to actually build versions instead of 1.23.0
  ([`50cff7e`](https://github.com/cbrand/micropython-mdns/commit/50cff7efc94506fbf3645b5e176d74de521ecad5))

- **Dockerfile**: Test fix for rp2 according to #26
  ([`5906dd5`](https://github.com/cbrand/micropython-mdns/commit/5906dd517753397d3351d9e3da6b0591d81589d8))

### Documentation

- Clarify on asyncio tasks implicitly started via query_once()
  ([`d66f00d`](https://github.com/cbrand/micropython-mdns/commit/d66f00d503da2583478a8f6e4ee1873934cce897))


## v1.5.0 (2024-10-15)

### Bug Fixes

- Requirements.txt to reduce vulnerabilities
  ([`1e3d040`](https://github.com/cbrand/micropython-mdns/commit/1e3d040c2a89220e97a2ce2949d8073d2aeaa236))

The following vulnerabilities are fixed by pinning transitive dependencies: -
  https://snyk.io/vuln/SNYK-PYTHON-ZIPP-7430899

- Requirements.txt to reduce vulnerabilities
  ([`56bbed8`](https://github.com/cbrand/micropython-mdns/commit/56bbed8532a68da66f7a4df731156d5be1282691))

The following vulnerabilities are fixed by pinning transitive dependencies: -
  https://snyk.io/vuln/SNYK-PYTHON-URLLIB3-7267250

- Requirements.txt to reduce vulnerabilities
  ([`e8d5e59`](https://github.com/cbrand/micropython-mdns/commit/e8d5e59539cf0720429a2fbd1cff3890857e2b13))

The following vulnerabilities are fixed by pinning transitive dependencies: -
  https://snyk.io/vuln/SNYK-PYTHON-URLLIB3-7267250

- Requirements.txt to reduce vulnerabilities
  ([`f4f3f29`](https://github.com/cbrand/micropython-mdns/commit/f4f3f2973c6804511289c1e2682650ad95e02add))

The following vulnerabilities are fixed by pinning transitive dependencies: -
  https://snyk.io/vuln/SNYK-PYTHON-REQUESTS-6928867

- Requirements.txt to reduce vulnerabilities
  ([`8e53ff8`](https://github.com/cbrand/micropython-mdns/commit/8e53ff828fef564ca1ecf2d0e38026033b08b0be))

The following vulnerabilities are fixed by pinning transitive dependencies: -
  https://snyk.io/vuln/SNYK-PYTHON-CERTIFI-3164749 -
  https://snyk.io/vuln/SNYK-PYTHON-CERTIFI-5805047 -
  https://snyk.io/vuln/SNYK-PYTHON-CRYPTOGRAPHY-3172287 -
  https://snyk.io/vuln/SNYK-PYTHON-CRYPTOGRAPHY-3314966 -
  https://snyk.io/vuln/SNYK-PYTHON-CRYPTOGRAPHY-3315324 -
  https://snyk.io/vuln/SNYK-PYTHON-CRYPTOGRAPHY-3315328 -
  https://snyk.io/vuln/SNYK-PYTHON-CRYPTOGRAPHY-3315331 -
  https://snyk.io/vuln/SNYK-PYTHON-CRYPTOGRAPHY-3315452 -
  https://snyk.io/vuln/SNYK-PYTHON-CRYPTOGRAPHY-3315972 -
  https://snyk.io/vuln/SNYK-PYTHON-CRYPTOGRAPHY-3315975 -
  https://snyk.io/vuln/SNYK-PYTHON-CRYPTOGRAPHY-3316038 -
  https://snyk.io/vuln/SNYK-PYTHON-CRYPTOGRAPHY-3316211 -
  https://snyk.io/vuln/SNYK-PYTHON-CRYPTOGRAPHY-5663682 -
  https://snyk.io/vuln/SNYK-PYTHON-CRYPTOGRAPHY-5777683 -
  https://snyk.io/vuln/SNYK-PYTHON-CRYPTOGRAPHY-5813745 -
  https://snyk.io/vuln/SNYK-PYTHON-CRYPTOGRAPHY-5813746 -
  https://snyk.io/vuln/SNYK-PYTHON-CRYPTOGRAPHY-5813750 -
  https://snyk.io/vuln/SNYK-PYTHON-CRYPTOGRAPHY-5914629 -
  https://snyk.io/vuln/SNYK-PYTHON-PYGMENTS-1086606 -
  https://snyk.io/vuln/SNYK-PYTHON-PYGMENTS-1088505 -
  https://snyk.io/vuln/SNYK-PYTHON-PYGMENTS-5750273 -
  https://snyk.io/vuln/SNYK-PYTHON-REQUESTS-5595532 -
  https://snyk.io/vuln/SNYK-PYTHON-SETUPTOOLS-3180412 -
  https://snyk.io/vuln/SNYK-PYTHON-WHEEL-3180413

- **record**: Lowercase all mdns records
  ([`f557fa0`](https://github.com/cbrand/micropython-mdns/commit/f557fa05d7d3226931222c2d7ddf2adb21780d78))

Following advice from https://github.com/cbrand/micropython-mdns/issues/24 make sure that only
  lowercase configurations are resolved making the library case insensitive.

### Chores

- **pre-commit-config**: Update pre commit versions
  ([`f3fae99`](https://github.com/cbrand/micropython-mdns/commit/f3fae99dd6e8aea9393c28d1940ca9f943b2ccd3))

- **README**: Add tips how to build RPI Pico with the library
  ([`ca5a95a`](https://github.com/cbrand/micropython-mdns/commit/ca5a95ac6f890b078ae9731ab1f5ac4e54367457))

### Features

- **boards**: Add compile support for raspberry pi micro
  ([`86670ac`](https://github.com/cbrand/micropython-mdns/commit/86670ac4041329a668b6cc63e7b3399339fa0977))

Add support for RPI builds and support for Micropython 1.21, 1.22 and 1.23 for esp32.

Fixes #15


## v1.4.0 (2023-09-21)

### Chores

- Add support for building on remote docker
  ([`d8cb40f`](https://github.com/cbrand/micropython-mdns/commit/d8cb40f0a9684869db3b5ce45f57bb6b2e779aea))

Adjust build scripts to work to retrieve the firmware on remote docker builds too.

- Drop support for Micropython 1.13
  ([`6f8c186`](https://github.com/cbrand/micropython-mdns/commit/6f8c186b5a4c045a9f02bc1844bece88efd85485))

Requires python 2 to build which is no longer supported.

- Fix semantic release config for new version
  ([`8ffb6f4`](https://github.com/cbrand/micropython-mdns/commit/8ffb6f4a35c5109185cda9940c8239acaecc0f95))

- Update Changelog with 1.3.0 changes
  ([`dcbf580`](https://github.com/cbrand/micropython-mdns/commit/dcbf580304e0ce1fb54a3e3b0d3594350ea2fd00))

- Update classifiers for pypi
  ([`159b7aa`](https://github.com/cbrand/micropython-mdns/commit/159b7aa4a202f6dd9ff3443d0add56f328ea8053))

- Update readme with compile targets
  ([`482148d`](https://github.com/cbrand/micropython-mdns/commit/482148d5d578cf62ebc90df1f9e08a1d6d5bb33f))

### Features

- Add mip package support
  ([`f7d6299`](https://github.com/cbrand/micropython-mdns/commit/f7d62992a0198db448fb431b9db90b9b3147cb5c))

Following configuration for
  https://docs.micropython.org/en/latest/reference/packages.html#writing-publishing-packages


## v1.3.0 (2023-09-20)

### Bug Fixes

- Make all imports absolute
  ([`bafe176`](https://github.com/cbrand/micropython-mdns/commit/bafe17626411ed934b10ba4dd7867d7c7187364c))

Fix which might help using the library in a frozen module.

- Requirements.txt to reduce vulnerabilities
  ([`c717474`](https://github.com/cbrand/micropython-mdns/commit/c7174746614458885f48d1f471e226b79c347871))

The following vulnerabilities are fixed by pinning transitive dependencies: -
  https://snyk.io/vuln/SNYK-PYTHON-WHEEL-3092128 - https://snyk.io/vuln/SNYK-PYTHON-WHEEL-3180413

### Chores

- Fix Dockerfile configuration
  ([`89f2e58`](https://github.com/cbrand/micropython-mdns/commit/89f2e58d8b02f6714985b080a74d3a0986a17770))

Remove the python installations in all Dockerfiles to allow building the project with newer docker
  files.

- Fix Makefile for other configs
  ([`c2bb1e7`](https://github.com/cbrand/micropython-mdns/commit/c2bb1e72486b191798b52e626c0475c9f414caa4))

Make tty interface configurable

- Update documentation for new advertise function
  ([`3b969b8`](https://github.com/cbrand/micropython-mdns/commit/3b969b8dab64ea33f92ea1920cdc02ce74b45529))

Add documentation to show how service_host_name in the advertise endpoint works.

### Features

- Add build for micropython 1.20
  ([`01b7996`](https://github.com/cbrand/micropython-mdns/commit/01b7996ac22db7879a22e86f21807259b617d125))

- Add support for configurable service hostnames
  ([`cc6169f`](https://github.com/cbrand/micropython-mdns/commit/cc6169ff06734befc5e042be6ee7768c8ff60904))

Instead of fixing the service host name to the hostname of the host, make it possible to add a new
  parameter `host` into the `advertise` function of the service and allow it to register its own
  advertised name in the service.

Usage example: ``` loop = uasyncio.get_event_loop() client = Client(own_ip_address) responder =
  Responder( client, own_ip=lambda: own_ip_address, host=lambda:
  "my-awesome-microcontroller-{}".format(responder.generate_random_postfix()), )

def announce_service(): responder.advertise("_myawesomeservice", "_tcp", port=12345, data={"some":
  "metadata", "for": ["my", "service"]}, service_host_name="myoverwrittenhost") ```


## v1.2.3 (2022-10-04)

### Bug Fixes

- Always return a txt dns record even if empty
  ([`e75757a`](https://github.com/cbrand/micropython-mdns/commit/e75757a024582221c66ac5f2832d040bfaa0dc4b))


## v1.2.2 (2022-10-04)

### Bug Fixes

- Skip null txt record
  ([`40d09b7`](https://github.com/cbrand/micropython-mdns/commit/40d09b7ad1bb5e785b7c8be3f04ac923043545ca))

Do not try to send a txt record when information for sending it out is missing. Before this if there
  was a TXT record request it did raise an Exception instead of just not returning the information.

### Chores

- Adjust reference example for better use
  ([`e7b1087`](https://github.com/cbrand/micropython-mdns/commit/e7b10874a95e1e99006dd2f0a3909fbeb042a1ae))

Use the generate_random_postfix call outside of the responder to let the example generate a
  consistent postfix for each request.

- Remove confusing test folder
  ([`7ab609e`](https://github.com/cbrand/micropython-mdns/commit/7ab609e4be51e0927db5dd2938e0ede3d617cabe))


## v1.2.1 (2022-10-03)

### Bug Fixes

- Correct name length package generation
  ([`9a9ddae`](https://github.com/cbrand/micropython-mdns/commit/9a9ddae780d3b34f29e275e724442c95d769d575))

Fixed an issue with name length generation for domain names which resulted into micropython-mdns
  creating wrongly formatted dns packages which couldn't be parsed by certain implementations of
  mdns like avahi.

Fixes #6


## v1.2.0 (2022-09-28)

### Bug Fixes

- Adjust release pipeline
  ([`1f96cf1`](https://github.com/cbrand/micropython-mdns/commit/1f96cf1ca2adb769b40d8d838165f5819c07f519))

- Responder dns ptr record zeroconf support
  ([`285d24b`](https://github.com/cbrand/micropython-mdns/commit/285d24b3b339a5c6fa9f46db4ae26129fe2a491e))

fixes #5

### Chores

- Adjust pyproject
  ([`e38a376`](https://github.com/cbrand/micropython-mdns/commit/e38a376bb52a9b13aa3a69bb18bdcd5b9fbe87e3))

- Fix changelog for 1.1.0
  ([`024d33f`](https://github.com/cbrand/micropython-mdns/commit/024d33fd205b80fd4d971d5a77c3adac30304993))

- Wording adjustments README
  ([`8ac3435`](https://github.com/cbrand/micropython-mdns/commit/8ac343545f34ea915ef43190c5f3347315d7e57e))

### Features

- Add compile targets for new micropython
  ([`2b15d01`](https://github.com/cbrand/micropython-mdns/commit/2b15d0198562b2a28537ffb4c7cdd822385e16ea))

Add support for micropython 1.18 and 1.19


## v1.1.0 (2022-01-06)

### Chores

- Add semantic release support
  ([`6aa4325`](https://github.com/cbrand/micropython-mdns/commit/6aa43258f8daba88d2c0c3f5c9b1328eed34f296))

### Features

- Add image for micropython 1.16 and 1.17
  ([`525ec39`](https://github.com/cbrand/micropython-mdns/commit/525ec3964ea6f5941ffa5032a330aaf6658f114d))


## v1.0.1 (2021-06-15)

### Chores

- **client**: Reinitialize socket on send failure
  ([`52b3ff9`](https://github.com/cbrand/micropython-mdns/commit/52b3ff9396880fdda81d54c32506b452c7ab3998))


## v1.0.0 (2021-04-26)

### Chores

- **examples**: Explicitly set wlan active flag
  ([`c7d0168`](https://github.com/cbrand/micropython-mdns/commit/c7d01682ad0fae39f9d6b1edd58b9b7380b18168))

- **pre-commit**: Update pre-commit config
  ([`50305a5`](https://github.com/cbrand/micropython-mdns/commit/50305a5f9ed399200e759fe6e451620dfe88693c))

- **README**: Add reference to MicroPython 1.15
  ([`549c594`](https://github.com/cbrand/micropython-mdns/commit/549c594c19f700ed35b2809f7364cb98db491bff))


## v0.9.3 (2021-01-06)


## v0.9.2 (2021-01-06)

### Bug Fixes

- **client**: Do not fail on error in packet processing
  ([`8fe0203`](https://github.com/cbrand/micropython-mdns/commit/8fe0203b1cc903eaa76c629ec28906c27f64ac99))


## v0.9.1 (2021-01-06)


## v0.9.0 (2021-01-06)

### Bug Fixes

- **client**: Handle memory issues on high traffic MDNS networks
  ([`8ee9488`](https://github.com/cbrand/micropython-mdns/commit/8ee94882d81d5bc17388ac4f75d7ee9ce59f816b))

- **parser**: Add possibility for nested name dereference
  ([`92f5b46`](https://github.com/cbrand/micropython-mdns/commit/92f5b4633e0428da9bcf72c69284a02acc468a50))

### Chores

- **debug**: Add better log debugging
  ([`03997cb`](https://github.com/cbrand/micropython-mdns/commit/03997cbebb60c318c80962ce8896c246f32c5eb9))

- **examples**: Add examples for library usage
  ([`eb1ac35`](https://github.com/cbrand/micropython-mdns/commit/eb1ac3502af4918ef522f76932e8f013f8141611))

- **REFERENCE**: Adjust shield colors
  ([`baf9589`](https://github.com/cbrand/micropython-mdns/commit/baf9589c13ec489284e91cafdc70aded7137b754))
