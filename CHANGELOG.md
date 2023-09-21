# CHANGELOG



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
