AFRAME.registerPrimitive('a-ocean', {
          defaultComponents: {
                    ocean: {},
                    rotation: { x: -90, y: 0, z: 0 }
          },
          mappings: {
                    width: 'ocean.width',
                    depth: 'ocean.depth',
                    density: 'ocean.density',
                    amplitude: 'ocean.amplitude',
                    amplitudeVariance: 'ocean.amplitudeVariance',
                    speed: 'ocean.speed',
                    speedVariance: 'ocean.speedVariance',
                    color: 'ocean.color',
                    opacity: 'ocean.opacity'
          }
});

AFRAME.registerComponent('oceanfixed', {
          schema: {
                    // Dimensions of the ocean area.
                    width: { default: 70, min: 0 },
                    depth: { default: 70, min: 0 },

                    // Density of waves.
                    density: { default: 8 },

                    // Wave amplitude and variance.
                    amplitude: { default: 0.2 },
                    amplitudeVariance: { default: 0.3 },

                    // Wave speed and variance.
                    speed: { default: 0.2 },
                    speedVariance: { default: 1 },

                    // Material.
                    color: { default: '#20a1f1', type: 'color' },
                    opacity: { default: 0.4}
          },

          /**
           * Use play() instead of init(), because component mappings – unavailable as dependencies – are
           * not guaranteed to have parsed when this component is initialized.
           */
          play: function () {
                    const el = this.el;
                    const data = this.data;
                    let material = el.components.material;

                    const geometry = new THREE.PlaneGeometry(data.width, data.depth, data.density, data.density);
                    this.waves = [];
                    const posAttribute = geometry.getAttribute('position');
                    for (let i = 0; i < posAttribute.count; i++) {
                              this.waves.push({
                                        z: posAttribute.getZ(i),
                                        ang: Math.random() * Math.PI * 2,
                                        amp: data.amplitude + Math.random() * data.amplitudeVariance,
                                        speed: (data.speed + Math.random() * data.speedVariance) / 1000 // radians / frame
                              });
                    }

                    if (!material) {
                              material = {};
                              material.material = new THREE.MeshPhongMaterial({
                                        color: data.color,
                                        transparent: data.opacity < 1,
                                        opacity: data.opacity,
                                        flatShading: true,
                              });
                    }

                    this.mesh = new THREE.Mesh(geometry, material.material);
                    el.setObject3D('mesh', this.mesh);
          },

          remove: function () {
                    this.el.removeObject3D('mesh');
          },

          tick: function (t, dt) {
                    if (!dt) return;

                    const posAttribute = this.mesh.geometry.getAttribute('position');
                    for (let i = 0; i < posAttribute.count; i++) {
                              const vprops = this.waves[i];
                              const value = vprops.z + Math.sin(vprops.ang) * vprops.amp;
                              posAttribute.setZ(i, value);
                              vprops.ang += vprops.speed * dt;
                    }
                    posAttribute.needsUpdate = true;
          }
});