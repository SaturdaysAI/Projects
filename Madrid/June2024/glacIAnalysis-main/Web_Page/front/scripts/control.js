function init() {
          const buttonInit = document.getElementById("init")
          buttonInit.remove();
          // MOVIMIENTO DE OSO
          const el = document.querySelector('[walk]');
          const model = el.getObject3D('mesh');
          if (model) {
                    el.components.walk.move(model, 4000);
          } else {
          el.addEventListener('model-loaded', function (e) {
                     el.components.walk.move(e.detail.model, 3000);
          });
          }
          el.setAttribute('animation', 'property: position; to: 0 0 -2; dur: 4000; easing: linear; loop: false');

          setTimeout(() => {
                    const intro = document.getElementById('introaudio');
                    intro.play();
          }, 4000);
          setTimeout(() => {
                    const more= document.getElementById('more');
                    more.style.display = 'inline';
          }, 25000);
}

function more() {
          const more = document.getElementById('more');
          more.remove()

          const networkEntity = document.getElementById('network');
          networkEntity.setAttribute('babia-network', 'nodeLegend', 'true');
          networkEntity.setAttribute('visible', 'true');

          const moreaudio = document.getElementById('moreaudio');
          moreaudio.play();

          setTimeout(() => {
                    const deep = document.getElementById('deep');
                    deep.style.display = 'inline';
          }, 15000);
}

function deep() {
          const deep = document.getElementById('deep');
          deep.remove()
          const deepaudio = document.getElementById('deepaudio');
          deepaudio.play();
}

AFRAME.registerComponent("walk", {
          init: function () {
                    this.model = null;
                    this.mixer = null;
          },
          move: function (model, duration) {
                    this.model = model;
                    this.mixer = new THREE.AnimationMixer(model);
                    this.model.animations.forEach((animation) => {
                              this.mixer.clipAction(animation, model).play();
                    });
                    setTimeout(() => {
                              this.model.animations.forEach((animation) => {
                                        this.mixer.clipAction(animation, model).stop();
                              });
                              speech(document.querySelector("#hello"));
                    }, duration);
          },
          tick: function (t, dt) {
                    if (this.mixer && !isNaN(dt)) {
                              this.mixer.update(dt / 1000);
                    }
          },
});

function isMobile() {
          return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
}

 function loadEntity() {
          if (!isMobile()) {
              const asset = document.createElement('a-asset-item');
              asset.setAttribute('id', 'background');
              asset.setAttribute('src', './assets/fondo.glb');
              document.querySelector('a-assets').appendChild(asset);

              const entity = document.createElement('a-entity');
              entity.setAttribute('gltf-model', '#background');
              entity.setAttribute('scale', '1 1 1');
              entity.setAttribute('position', '0 0 0');
              entity.setAttribute('rotation', '0 220 0');
              document.querySelector('a-scene').appendChild(entity);
          }
}

document.addEventListener('DOMContentLoaded', loadEntity);