# CHANGELOG



## v1.8.0 (2025-12-29)

### Chore

* chore: inline private helper used only once and remove redundant close

Improves code size and speed. close is done by __init_socket() anyway. ([`56b3c14`](https://github.com/cbrand/micropython-mdns/commit/56b3c14c4616213c85d4a85011c0a03f23703f95))

### Feature

* feat(Makefile): add support for micropython 1.27 ([`d1aa2d7`](https://github.com/cbrand/micropython-mdns/commit/d1aa2d7d7b04301d0856cc3e146653ba201f14c9))

* feat: add method for re-adding multicast membership by user code

Now a user can call add_membership() without arguments to add multicast membership again, e.g. after reconnecting to the network. ([`9865375`](https://github.com/cbrand/micropython-mdns/commit/98653758ef496772a3369aff9c0f1a6ec5e46937))

### Fix

* fix(setup): adjust egg name to acceptable version ([`efa6110`](https://github.com/cbrand/micropython-mdns/commit/efa6110f69bc4a0025626a2eee8cd96028b228eb))

* fix(Dockerfile): to support micropython 1.25 downgrade to 3.11 ([`b166f26`](https://github.com/cbrand/micropython-mdns/commit/b166f26ebeceb06300c1b2eebc93967967010099))

* fix: prevent Client.start() from running multiple times

To prevent glitches also clear the &#34;stopped&#34; flag only in start() and initialize the socket just before the consume loop that uses it. ([`c271f81`](https://github.com/cbrand/micropython-mdns/commit/c271f810e654c7e076b16e68ef03023b73ea84f6))

* fix: prevent MemoryError by switching tasks before receiving data ([`31a9e62`](https://github.com/cbrand/micropython-mdns/commit/31a9e6254370e4a4cfc65ee8c3543e16ad33d8e3))

* fix: handle OSError from second sendto()

Prevents a crash of discovery._change_loop(). ([`62ff125`](https://github.com/cbrand/micropython-mdns/commit/62ff125e76160220339385efb6b09f8f48374cd0))

### Unknown

* Merge pull request #37 from oliver-joos/add-membership-after-reconnect

Add multicast membership again after reconnecting network ([`ede399c`](https://github.com/cbrand/micropython-mdns/commit/ede399cbdcba628f00bb0099ae90b73e3ab4c3b7))

* Merge pull request #39 from oliver-joos/handle-socket-errors

Prevent or handle socket errors ([`219b847`](https://github.com/cbrand/micropython-mdns/commit/219b847167a591361615efa3bf1eb7ef809a148f))


## v1.7.1 (2025-10-09)

### Chore

* chore: bump version in code ([`bbabcd5`](https://github.com/cbrand/micropython-mdns/commit/bbabcd516fe50e19cdc58a9b7dcbcf1c32e6d013))

### Unknown

* Version 1.7.1 ([`8b70e35`](https://github.com/cbrand/micropython-mdns/commit/8b70e3567c35a4df6c89e083c3d5d6e5fdcf44c0))

* Merge pull request #21 from cbrand/snyk-fix-6fc01ce2b2862a0351fb90cc277432ba

[Snyk] Security upgrade setuptools from 68.0.0 to 70.0.0 ([`d421a9e`](https://github.com/cbrand/micropython-mdns/commit/d421a9e98429257016028788d6a8631fed8085d7))

* Merge branch &#39;main&#39; into snyk-fix-6fc01ce2b2862a0351fb90cc277432ba ([`e7f9b85`](https://github.com/cbrand/micropython-mdns/commit/e7f9b8526be98f48207621e7534ffd909fb22197))


## v1.7.0 (2025-10-09)

### Chore

* chore(Dockerfile): bump 1.25 to 1.26 for rp2 down to python 3:11 ([`73960aa`](https://github.com/cbrand/micropython-mdns/commit/73960aa743c88f1b97fbdc1b81181b3bb0dd924a))

* chore(Dockerfile): update python base image to 3.12 for 1.25 and 1.26 build ([`3bd1aba`](https://github.com/cbrand/micropython-mdns/commit/3bd1aba9a05a2cf377351aaee610a9d567f50133))

* chore(Dockerfile): update micropython config ([`54ec87f`](https://github.com/cbrand/micropython-mdns/commit/54ec87f206f55bacc3f29c33416ab97783bf31bf))

* chore: Fix changelog for 1.6.0 version ([`0fb235f`](https://github.com/cbrand/micropython-mdns/commit/0fb235f0ba5a06ecba82eac305eb0029f46c0fb7))

* chore(README): remove upip reference ([`ec9bafa`](https://github.com/cbrand/micropython-mdns/commit/ec9bafa3cf4a3970cf81dafeeb84ccdb034376d0))

* chore: remove unused sdist_upip ([`57210d0`](https://github.com/cbrand/micropython-mdns/commit/57210d0ea9e1085b4ea1820fe02cb11c795c5fcb))

### Feature

* feat(1.26): fix builds for micropython 1.26 ([`cb5ed02`](https://github.com/cbrand/micropython-mdns/commit/cb5ed025a8fb69437e77244ad8f6396d75fa8df4))

* feat(service_discovery): add feature flag to enable dns-sd on queries

It seems that some devices require a dns-sd query to return
a response from a service query.

See: https://github.com/cbrand/micropython-mdns/issues/34 for details ([`e1ec88c`](https://github.com/cbrand/micropython-mdns/commit/e1ec88cb7ced38a42caa9c53301124175da1accd))

* feat: add support for micropython 1.25 and 1.26 ([`d4cf4e8`](https://github.com/cbrand/micropython-mdns/commit/d4cf4e8788d82e2a39e9ae1ce4c57c8ce94dad9e))

### Fix

* fix(Dockerfile): micropython config ([`7152dd9`](https://github.com/cbrand/micropython-mdns/commit/7152dd97936de2c188326a0955946fea61d9aaed))

* fix: requirements.txt to reduce vulnerabilities


The following vulnerabilities are fixed by pinning transitive dependencies:
- https://snyk.io/vuln/SNYK-PYTHON-URLLIB3-10390193
- https://snyk.io/vuln/SNYK-PYTHON-URLLIB3-10390194 ([`5a7817f`](https://github.com/cbrand/micropython-mdns/commit/5a7817ffc0a128b49608048559e37609f6c9fa7c))

* fix: requirements.txt to reduce vulnerabilities


The following vulnerabilities are fixed by pinning transitive dependencies:
- https://snyk.io/vuln/SNYK-PYTHON-REQUESTS-10305723 ([`9852bed`](https://github.com/cbrand/micropython-mdns/commit/9852bed255a704e1b5f1f678591237962cc8e2d2))

### Unknown

* Merge pull request #32 from cbrand/snyk-fix-332a36f2e06bec142b4ce7d6c58f720c

[Snyk] Security upgrade requests from 2.31.0 to 2.32.4 ([`9c58ce2`](https://github.com/cbrand/micropython-mdns/commit/9c58ce249169988e528341d711796f33acffae54))

* Merge pull request #33 from cbrand/snyk-fix-394dcaea770dc8c0870fc84883c20634

[Snyk] Security upgrade urllib3 from 2.0.7 to 2.5.0 ([`0423d3f`](https://github.com/cbrand/micropython-mdns/commit/0423d3f9994be61f0037416749498774ed2878fd))


## v1.6.0 (2025-01-19)

### Chore

* chore(Makefile): rebuild build system to compile during runtime and not build time for rp2 and esp32 builds ([`0aa5f9a`](https://github.com/cbrand/micropython-mdns/commit/0aa5f9a88534d17bff4a65b669f034dadd8cd4d5))

* chore: adjust reference config ([`7385fb8`](https://github.com/cbrand/micropython-mdns/commit/7385fb8a9404f25e178df942dbe90805c9d1a199))

* chore: update Makefile

fix various configs in the Makefile and add Micropython 1.24 (hacked)
support. ([`1503bfa`](https://github.com/cbrand/micropython-mdns/commit/1503bfa0cfed6203b41594c931ca0c0411957790))

### Fix

* fix(mdns_client): support for rp2 on 1.24

As reported in https://github.com/cbrand/micropython-mdns/pull/30 there were issues even after the patches wtih the 1.24 version of resolving MDNS. This was due to the socket binding not being bound to the MDNS address. Both on the ESP32 and the RP2 with 1.24 binding works now again.

To not have a backwards issue with the code base, dropping support for anything older than 1.24 in this commit and in the next release. ([`6d09fba`](https://github.com/cbrand/micropython-mdns/commit/6d09fbacc50b75e31773378f2ec098351b3bfc99))

* fix(service_discovery): adjust discover_once to shut down resources

If the discover_once method is called and the underyling client
and / or discovery has not been started by another component
ensure to shut down the complete library afterwards to not consume
any resources without a developer explicitly asking for other
functionality in the MDNS library. ([`2331707`](https://github.com/cbrand/micropython-mdns/commit/233170773933aa2de63b10cedbe3daf9392dff15))

* fix(service_discovery): a record detection for certain devices

Ensure that the A record for certain devices (for example shellies)
is done correctly by buffering currently irrelevant A records as
they get sent before the SRV record for the specific target is sent.

This change slightly increases memory overhead as an additional
configurable buffer needs to be added to allow buffering A
records which are not yet relevant for an SRV response. ([`078f3df`](https://github.com/cbrand/micropython-mdns/commit/078f3df5cb44b4438049a26431ae09aea48b7624))

### Unknown

* Version 1.6.0 ([`a3b0677`](https://github.com/cbrand/micropython-mdns/commit/a3b0677d543241caa744ee5364d68f0140261613))

* Merge pull request #30 from joncard1/docker-rp2-fix

Updated the sed command ([`6791b3e`](https://github.com/cbrand/micropython-mdns/commit/6791b3e923f287255bb642549775872c68369029))

* Updated the sed command

Without the &#34;-i&#34; switch, the underlying file is not affected, and the &#34;$&#34; introduced a typo in the C file. ([`26629f3`](https://github.com/cbrand/micropython-mdns/commit/26629f326665a45835d5a59f796d4b3382b89e94))

* Version 1.5.2 ([`a255ecb`](https://github.com/cbrand/micropython-mdns/commit/a255ecbc8189e63392a84445d86eec277f1f0a4e))


## v1.5.1 (2024-12-15)

### Chore

* chore(Dockerfile): test fix for rp2 according to #26 ([`5906dd5`](https://github.com/cbrand/micropython-mdns/commit/5906dd517753397d3351d9e3da6b0591d81589d8))

* chore(Dockerfile): fix esp32 buidls for 1.21 and 1.22 to actually build versions instead of 1.23.0 ([`50cff7e`](https://github.com/cbrand/micropython-mdns/commit/50cff7efc94506fbf3645b5e176d74de521ecad5))

* chore(Dockerfile): add support for rp2 build for micropython 1.22 ([`e009cfb`](https://github.com/cbrand/micropython-mdns/commit/e009cfbd276734bd5754b36da8ea8e1e35488974))

### Documentation

* docs: clarify on asyncio tasks implicitly started via query_once() ([`d66f00d`](https://github.com/cbrand/micropython-mdns/commit/d66f00d503da2583478a8f6e4ee1873934cce897))

### Fix

* fix(service_discovery): stop discovery loop on stopped client

The service discovery did not take into account that the client might have shut down in between, resulting in a loop running forever reinitializing manually closed clients resulting in unexplainable error messages. ([`5bf8419`](https://github.com/cbrand/micropython-mdns/commit/5bf8419e1b0b5fa59da48198f8b20b6624477520))

* fix(Docker): fix build files for rp2 versions

copy correct file over with the correct configuration. ([`2ed23d4`](https://github.com/cbrand/micropython-mdns/commit/2ed23d457a691656ecab3e4ea824b6cf10cbecba))

### Unknown

* Version 1.5.1 ([`e23708b`](https://github.com/cbrand/micropython-mdns/commit/e23708bbf9d0e6a1809a2cebe46cf4ac7bc69947))

* Merge pull request #28 from mirko/clarify-on-query_once

docs: clarify on asyncio tasks implicitly started via query_once() ([`a3dc0c2`](https://github.com/cbrand/micropython-mdns/commit/a3dc0c240adc40303764d48aa478b4c5782c56fe))

* Merge pull request #23 from cbrand/snyk-fix-c864f9ede7c3cb1285cdcffa04300a91

[Snyk] Security upgrade zipp from 3.15.0 to 3.19.1 ([`e50b196`](https://github.com/cbrand/micropython-mdns/commit/e50b196012a816cf61f39fdb04cee86380be294c))


## v1.5.0 (2024-10-15)

### Chore

* chore(pre-commit-config): update pre commit versions ([`f3fae99`](https://github.com/cbrand/micropython-mdns/commit/f3fae99dd6e8aea9393c28d1940ca9f943b2ccd3))

* chore(README): add tips how to build RPI Pico with the library ([`ca5a95a`](https://github.com/cbrand/micropython-mdns/commit/ca5a95ac6f890b078ae9731ab1f5ac4e54367457))

### Feature

* feat(boards): add compile support for raspberry pi micro

Add support for RPI builds and support for Micropython 1.21, 1.22 and 1.23 for esp32.

Fixes #15 ([`86670ac`](https://github.com/cbrand/micropython-mdns/commit/86670ac4041329a668b6cc63e7b3399339fa0977))

### Fix

* fix(record): lowercase all mdns records

Following advice from https://github.com/cbrand/micropython-mdns/issues/24 make sure that only lowercase configurations are resolved making the library case insensitive. ([`f557fa0`](https://github.com/cbrand/micropython-mdns/commit/f557fa05d7d3226931222c2d7ddf2adb21780d78))

* fix: requirements.txt to reduce vulnerabilities


The following vulnerabilities are fixed by pinning transitive dependencies:
- https://snyk.io/vuln/SNYK-PYTHON-ZIPP-7430899 ([`819b300`](https://github.com/cbrand/micropython-mdns/commit/819b300355cd21bac6092e87fa30051a87f249f2))

* fix: requirements.txt to reduce vulnerabilities


The following vulnerabilities are fixed by pinning transitive dependencies:
- https://snyk.io/vuln/SNYK-PYTHON-SETUPTOOLS-7448482 ([`bf96ca1`](https://github.com/cbrand/micropython-mdns/commit/bf96ca1d89c943cdd0e6d924a496035675c0b479))

* fix: requirements.txt to reduce vulnerabilities


The following vulnerabilities are fixed by pinning transitive dependencies:
- https://snyk.io/vuln/SNYK-PYTHON-ZIPP-7430899 ([`1e3d040`](https://github.com/cbrand/micropython-mdns/commit/1e3d040c2a89220e97a2ce2949d8073d2aeaa236))

* fix: requirements.txt to reduce vulnerabilities


The following vulnerabilities are fixed by pinning transitive dependencies:
- https://snyk.io/vuln/SNYK-PYTHON-URLLIB3-7267250 ([`56bbed8`](https://github.com/cbrand/micropython-mdns/commit/56bbed8532a68da66f7a4df731156d5be1282691))

* fix: requirements.txt to reduce vulnerabilities


The following vulnerabilities are fixed by pinning transitive dependencies:
- https://snyk.io/vuln/SNYK-PYTHON-URLLIB3-7267250 ([`e8d5e59`](https://github.com/cbrand/micropython-mdns/commit/e8d5e59539cf0720429a2fbd1cff3890857e2b13))

* fix: requirements.txt to reduce vulnerabilities


The following vulnerabilities are fixed by pinning transitive dependencies:
- https://snyk.io/vuln/SNYK-PYTHON-REQUESTS-6928867 ([`f4f3f29`](https://github.com/cbrand/micropython-mdns/commit/f4f3f2973c6804511289c1e2682650ad95e02add))

* fix: requirements.txt to reduce vulnerabilities


The following vulnerabilities are fixed by pinning transitive dependencies:
- https://snyk.io/vuln/SNYK-PYTHON-CERTIFI-3164749
- https://snyk.io/vuln/SNYK-PYTHON-CERTIFI-5805047
- https://snyk.io/vuln/SNYK-PYTHON-CRYPTOGRAPHY-3172287
- https://snyk.io/vuln/SNYK-PYTHON-CRYPTOGRAPHY-3314966
- https://snyk.io/vuln/SNYK-PYTHON-CRYPTOGRAPHY-3315324
- https://snyk.io/vuln/SNYK-PYTHON-CRYPTOGRAPHY-3315328
- https://snyk.io/vuln/SNYK-PYTHON-CRYPTOGRAPHY-3315331
- https://snyk.io/vuln/SNYK-PYTHON-CRYPTOGRAPHY-3315452
- https://snyk.io/vuln/SNYK-PYTHON-CRYPTOGRAPHY-3315972
- https://snyk.io/vuln/SNYK-PYTHON-CRYPTOGRAPHY-3315975
- https://snyk.io/vuln/SNYK-PYTHON-CRYPTOGRAPHY-3316038
- https://snyk.io/vuln/SNYK-PYTHON-CRYPTOGRAPHY-3316211
- https://snyk.io/vuln/SNYK-PYTHON-CRYPTOGRAPHY-5663682
- https://snyk.io/vuln/SNYK-PYTHON-CRYPTOGRAPHY-5777683
- https://snyk.io/vuln/SNYK-PYTHON-CRYPTOGRAPHY-5813745
- https://snyk.io/vuln/SNYK-PYTHON-CRYPTOGRAPHY-5813746
- https://snyk.io/vuln/SNYK-PYTHON-CRYPTOGRAPHY-5813750
- https://snyk.io/vuln/SNYK-PYTHON-CRYPTOGRAPHY-5914629
- https://snyk.io/vuln/SNYK-PYTHON-PYGMENTS-1086606
- https://snyk.io/vuln/SNYK-PYTHON-PYGMENTS-1088505
- https://snyk.io/vuln/SNYK-PYTHON-PYGMENTS-5750273
- https://snyk.io/vuln/SNYK-PYTHON-REQUESTS-5595532
- https://snyk.io/vuln/SNYK-PYTHON-SETUPTOOLS-3180412
- https://snyk.io/vuln/SNYK-PYTHON-WHEEL-3180413 ([`8e53ff8`](https://github.com/cbrand/micropython-mdns/commit/8e53ff828fef564ca1ecf2d0e38026033b08b0be))

### Unknown

* Merge pull request #20 from cbrand/snyk-fix-c864f9ede7c3cb1285cdcffa04300a91

[Snyk] Security upgrade zipp from 3.15.0 to 3.19.1 ([`22fc426`](https://github.com/cbrand/micropython-mdns/commit/22fc426c7752c22114f8e3aa268f080245deae81))

* Merge pull request #19 from cbrand/snyk-fix-04152d14a55fb78486714d72a4e45d1b

[Snyk] Security upgrade urllib3 from 2.0.7 to 2.2.2 ([`9bd4d75`](https://github.com/cbrand/micropython-mdns/commit/9bd4d75c4b2613c801a347c730b7c72eac64b3d5))

* Merge pull request #18 from cbrand/snyk-fix-e4c95849946480482bb5309de9885477

[Snyk] Security upgrade urllib3 from 2.0.7 to 2.2.2 ([`cc5b20d`](https://github.com/cbrand/micropython-mdns/commit/cc5b20d8635baad6feb7d2b198a7c57bbec4c086))

* Merge pull request #17 from cbrand/snyk-fix-2aa89ccd85b84e2ba5c7fba41b579086

[Snyk] Security upgrade requests from 2.31.0 to 2.32.0 ([`6dd7334`](https://github.com/cbrand/micropython-mdns/commit/6dd73348371215222f9b2cbc48340fed552f6411))

* Merge pull request #14 from cbrand/snyk-fix-8408080548f89d86210ea656f1fdd070

[Snyk] Fix for 24 vulnerabilities ([`eba8c10`](https://github.com/cbrand/micropython-mdns/commit/eba8c10c97b2a294bf2b3de326eab0a6b65d2e05))


## v1.4.0 (2023-09-21)

### Chore

* chore: fix semantic release config for new version ([`8ffb6f4`](https://github.com/cbrand/micropython-mdns/commit/8ffb6f4a35c5109185cda9940c8239acaecc0f95))

* chore: update readme with compile targets ([`482148d`](https://github.com/cbrand/micropython-mdns/commit/482148d5d578cf62ebc90df1f9e08a1d6d5bb33f))

* chore: add support for building on remote docker

Adjust build scripts to work to retrieve the firmware
on remote docker builds too. ([`d8cb40f`](https://github.com/cbrand/micropython-mdns/commit/d8cb40f0a9684869db3b5ce45f57bb6b2e779aea))

* chore: update Changelog with 1.3.0 changes ([`dcbf580`](https://github.com/cbrand/micropython-mdns/commit/dcbf580304e0ce1fb54a3e3b0d3594350ea2fd00))

* chore: drop support for Micropython 1.13

Requires python 2 to build which is no longer supported. ([`6f8c186`](https://github.com/cbrand/micropython-mdns/commit/6f8c186b5a4c045a9f02bc1844bece88efd85485))

* chore: update classifiers for pypi ([`159b7aa`](https://github.com/cbrand/micropython-mdns/commit/159b7aa4a202f6dd9ff3443d0add56f328ea8053))

### Feature

* feat: add mip package support

Following configuration for
https://docs.micropython.org/en/latest/reference/packages.html#writing-publishing-packages ([`f7d6299`](https://github.com/cbrand/micropython-mdns/commit/f7d62992a0198db448fb431b9db90b9b3147cb5c))


## v1.3.0 (2023-09-20)

### Chore

* chore: update documentation for new advertise function

Add documentation to show how service_host_name
in the advertise endpoint works. ([`3b969b8`](https://github.com/cbrand/micropython-mdns/commit/3b969b8dab64ea33f92ea1920cdc02ce74b45529))

* chore: fix Makefile for other configs

Make tty interface configurable ([`c2bb1e7`](https://github.com/cbrand/micropython-mdns/commit/c2bb1e72486b191798b52e626c0475c9f414caa4))

* chore: fix Dockerfile configuration

Remove the python installations in all Dockerfiles to allow
building the project with newer docker files. ([`89f2e58`](https://github.com/cbrand/micropython-mdns/commit/89f2e58d8b02f6714985b080a74d3a0986a17770))

### Feature

* feat: add support for configurable service hostnames

Instead of fixing the service host name to the hostname
of the host, make it possible to add a new parameter
`host` into the `advertise` function of the service and allow it to
register its own advertised name in the service.

Usage example:
```
loop = uasyncio.get_event_loop()
client = Client(own_ip_address)
responder = Responder(
    client,
    own_ip=lambda: own_ip_address,
    host=lambda: &#34;my-awesome-microcontroller-{}&#34;.format(responder.generate_random_postfix()),
)

def announce_service():
    responder.advertise(&#34;_myawesomeservice&#34;, &#34;_tcp&#34;, port=12345, data={&#34;some&#34;: &#34;metadata&#34;, &#34;for&#34;: [&#34;my&#34;, &#34;service&#34;]}, service_host_name=&#34;myoverwrittenhost&#34;)
``` ([`cc6169f`](https://github.com/cbrand/micropython-mdns/commit/cc6169ff06734befc5e042be6ee7768c8ff60904))

* feat: add build for micropython 1.20 ([`01b7996`](https://github.com/cbrand/micropython-mdns/commit/01b7996ac22db7879a22e86f21807259b617d125))

### Fix

* fix: make all imports absolute

Fix which might help using the library in a frozen module. ([`bafe176`](https://github.com/cbrand/micropython-mdns/commit/bafe17626411ed934b10ba4dd7867d7c7187364c))

* fix: requirements.txt to reduce vulnerabilities


The following vulnerabilities are fixed by pinning transitive dependencies:
- https://snyk.io/vuln/SNYK-PYTHON-WHEEL-3092128
- https://snyk.io/vuln/SNYK-PYTHON-WHEEL-3180413 ([`c717474`](https://github.com/cbrand/micropython-mdns/commit/c7174746614458885f48d1f471e226b79c347871))

### Unknown

* Version 1.3.0 ([`afe2f04`](https://github.com/cbrand/micropython-mdns/commit/afe2f04d764954e9c606fac90b69649c94dca020))

* Merge pull request #7 from cbrand/snyk-fix-7f31355a1fdab2fb82c5f78ff819d38f

[Snyk] Security upgrade wheel from 0.30.0 to 0.38.0 ([`8a92073`](https://github.com/cbrand/micropython-mdns/commit/8a920730cae49437a589bda6c95401a9f14561ec))


## v1.2.3 (2022-10-04)

### Fix

* fix: always return a txt dns record even if empty ([`e75757a`](https://github.com/cbrand/micropython-mdns/commit/e75757a024582221c66ac5f2832d040bfaa0dc4b))


## v1.2.2 (2022-10-04)

### Chore

* chore: adjust reference example for better use

Use the generate_random_postfix call outside of the responder
to let the example generate a consistent postfix
for each request. ([`e7b1087`](https://github.com/cbrand/micropython-mdns/commit/e7b10874a95e1e99006dd2f0a3909fbeb042a1ae))

* chore: remove confusing test folder ([`7ab609e`](https://github.com/cbrand/micropython-mdns/commit/7ab609e4be51e0927db5dd2938e0ede3d617cabe))

### Fix

* fix: skip null txt record

Do not try to send a txt record when information for sending
it out is missing. Before this if there was a TXT record request
it did raise an Exception instead of just not returning
the information. ([`40d09b7`](https://github.com/cbrand/micropython-mdns/commit/40d09b7ad1bb5e785b7c8be3f04ac923043545ca))


## v1.2.1 (2022-10-03)

### Fix

* fix: correct name length package generation

Fixed an issue with name length generation for domain names
which resulted into micropython-mdns creating wrongly
formatted dns packages which couldn&#39;t be parsed by
certain implementations of mdns like avahi.

Fixes #6 ([`9a9ddae`](https://github.com/cbrand/micropython-mdns/commit/9a9ddae780d3b34f29e275e724442c95d769d575))


## v1.2.0 (2022-09-27)

### Chore

* chore: wording adjustments README ([`8ac3435`](https://github.com/cbrand/micropython-mdns/commit/8ac343545f34ea915ef43190c5f3347315d7e57e))

* chore: fix changelog for 1.1.0 ([`024d33f`](https://github.com/cbrand/micropython-mdns/commit/024d33fd205b80fd4d971d5a77c3adac30304993))

* chore: adjust pyproject ([`e38a376`](https://github.com/cbrand/micropython-mdns/commit/e38a376bb52a9b13aa3a69bb18bdcd5b9fbe87e3))

### Feature

* feat: add compile targets for new micropython

Add support for micropython 1.18 and 1.19 ([`2b15d01`](https://github.com/cbrand/micropython-mdns/commit/2b15d0198562b2a28537ffb4c7cdd822385e16ea))

### Fix

* fix: responder dns ptr record zeroconf support

fixes #5 ([`285d24b`](https://github.com/cbrand/micropython-mdns/commit/285d24b3b339a5c6fa9f46db4ae26129fe2a491e))

* fix: adjust release pipeline ([`1f96cf1`](https://github.com/cbrand/micropython-mdns/commit/1f96cf1ca2adb769b40d8d838165f5819c07f519))

### Unknown

* Merge pull request #4 from hakancelikdev/patch-1

Fix unimport linter repo URL. ([`a3e0d47`](https://github.com/cbrand/micropython-mdns/commit/a3e0d47f1f9e760e088fbfc71c1467119e069b66))

* Fix unimport linter repo URL. ([`c5a044b`](https://github.com/cbrand/micropython-mdns/commit/c5a044b7c5bf3d03946b04c069bf2a2235cce258))


## v1.1.0 (2022-01-06)

### Chore

* chore: add semantic release support ([`6aa4325`](https://github.com/cbrand/micropython-mdns/commit/6aa43258f8daba88d2c0c3f5c9b1328eed34f296))

### Feature

* feat: add image for micropython 1.16 and 1.17 ([`525ec39`](https://github.com/cbrand/micropython-mdns/commit/525ec3964ea6f5941ffa5032a330aaf6658f114d))

### Unknown

* Merge pull request #3 from bgamari/patch-1

docs/REFERENCE: Fix erroneous example ([`812e296`](https://github.com/cbrand/micropython-mdns/commit/812e296dac816f14b2b6a6f162ec3cb3b6ab1865))

* docs/REFERENCE: Fix erroneous example

The `host_name` argument is actually called `host`. ([`30f8726`](https://github.com/cbrand/micropython-mdns/commit/30f872621eb469bb3dda3cbf2fc4721d822e6ca9))


## v1.0.1 (2021-06-15)

### Chore

* chore(client): reinitialize socket on send failure ([`52b3ff9`](https://github.com/cbrand/micropython-mdns/commit/52b3ff9396880fdda81d54c32506b452c7ab3998))

### Unknown

* Version 1.0.1 ([`b1a9473`](https://github.com/cbrand/micropython-mdns/commit/b1a9473cd5200e97ee578be4c623bbd610f46b6c))


## v1.0.0 (2021-04-25)

### Chore

* chore(pre-commit): update pre-commit config ([`50305a5`](https://github.com/cbrand/micropython-mdns/commit/50305a5f9ed399200e759fe6e451620dfe88693c))

* chore(README): add reference to MicroPython 1.15 ([`549c594`](https://github.com/cbrand/micropython-mdns/commit/549c594c19f700ed35b2809f7364cb98db491bff))

* chore(examples): explicitly set wlan active flag ([`c7d0168`](https://github.com/cbrand/micropython-mdns/commit/c7d01682ad0fae39f9d6b1edd58b9b7380b18168))

### Unknown

* Version 1.0.0 ([`021ecc2`](https://github.com/cbrand/micropython-mdns/commit/021ecc208330a7e0fc35bb94f2d2c8798a1aa106))

* Merge branch &#39;feature/micropython-1-15&#39; ([`6b2c79e`](https://github.com/cbrand/micropython-mdns/commit/6b2c79e05cccf443f52dff105951abb2cf07d2de))

* feature(Dockerfile): add support for micropython 1.15 ([`c99657d`](https://github.com/cbrand/micropython-mdns/commit/c99657da751a53eb47c96a2ea0a0593a61a25d48))


## v0.9.3 (2021-01-06)

### Unknown

* Version 0.9.3 ([`050be7f`](https://github.com/cbrand/micropython-mdns/commit/050be7f5dee11d0002b6d5f960d76e06eaa42560))

* feature(README): add intended audience section

Also use FQDNs for all links, making the
README to also be fully functionality on PyPi. ([`f579c47`](https://github.com/cbrand/micropython-mdns/commit/f579c47c58c9281af274e2848670016a21728765))


## v0.9.2 (2021-01-05)

### Fix

* fix(client): do not fail on error in packet processing ([`8fe0203`](https://github.com/cbrand/micropython-mdns/commit/8fe0203b1cc903eaa76c629ec28906c27f64ac99))

### Unknown

* Version 0.9.2 ([`b9b7379`](https://github.com/cbrand/micropython-mdns/commit/b9b73790ab2a5a90a60f5c550cde2eac36ed4b9d))

* Version 0.9.2 ([`f95873b`](https://github.com/cbrand/micropython-mdns/commit/f95873bc4ff2b1d870889b560917c0fa4ebe7bd9))


## v0.9.1 (2021-01-05)

### Unknown

* Version 0.9.1 ([`e9afc26`](https://github.com/cbrand/micropython-mdns/commit/e9afc2615fb47b658e1e0c7cb042d97b00b2a3e9))


## v0.9.0 (2021-01-05)

### Chore

* chore(REFERENCE): adjust shield colors ([`baf9589`](https://github.com/cbrand/micropython-mdns/commit/baf9589c13ec489284e91cafdc70aded7137b754))

* chore(examples): add examples for library usage ([`eb1ac35`](https://github.com/cbrand/micropython-mdns/commit/eb1ac3502af4918ef522f76932e8f013f8141611))

* chore(debug): add better log debugging ([`03997cb`](https://github.com/cbrand/micropython-mdns/commit/03997cbebb60c318c80962ce8896c246f32c5eb9))

### Fix

* fix(client): handle memory issues on high traffic MDNS networks ([`8ee9488`](https://github.com/cbrand/micropython-mdns/commit/8ee94882d81d5bc17388ac4f75d7ee9ce59f816b))

* fix(parser): add possibility for nested name dereference ([`92f5b46`](https://github.com/cbrand/micropython-mdns/commit/92f5b4633e0428da9bcf72c69284a02acc468a50))

### Unknown

* feature(README): add gif header ([`bc76e3f`](https://github.com/cbrand/micropython-mdns/commit/bc76e3fababa099326053d53127c230da54ea0f4))

* Version 0.9.0 ([`bce2e9a`](https://github.com/cbrand/micropython-mdns/commit/bce2e9afd4989b5da86e5f02192cbdba7695a757))

* feature(README): add README and LICENSE ([`2bc5318`](https://github.com/cbrand/micropython-mdns/commit/2bc53185d23b86103622eabe5ff09aebf7bd561f))

* feature(mdns_client): add response to service discovery call ([`321cb52`](https://github.com/cbrand/micropython-mdns/commit/321cb52e740f954f189fc7739b970ffce267d633))

* feature(responder): implement mdns service responder ([`d3dd54f`](https://github.com/cbrand/micropython-mdns/commit/d3dd54f809629ca41c525f5dec86963a6d75e903))

* feature(discovery): add optional txt extraction for service discovery ([`aaa9f61`](https://github.com/cbrand/micropython-mdns/commit/aaa9f614425047f49e210d6536ecddb8ddda8322))

* feature(discovery): implement first version of mdns service discovery ([`2f2f74e`](https://github.com/cbrand/micropython-mdns/commit/2f2f74ed42710ec809ce976ea497f474ec5f3137))

* feature(client): add mdns compatible getaddrinfo resolve ([`93fc389`](https://github.com/cbrand/micropython-mdns/commit/93fc38959d76b897234b7e573e35e5a6779d8bd7))

* feature(parser): implement proper name expansion ([`1459f64`](https://github.com/cbrand/micropython-mdns/commit/1459f64d1c4a00ecb8df987a229d09682363322e))

* feature(mdns_client): add basic mdns client ([`1428a89`](https://github.com/cbrand/micropython-mdns/commit/1428a89ad01cd272d2ce934aa46188501eefc9fb))
