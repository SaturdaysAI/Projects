AFRAME.registerShader('water-shader', {
    schema: {
        color: { type: 'color', is: 'uniform' },
        timeMsec: { type: 'time', is: 'uniform' },
        alpha: { type: 'number', is: 'uniform', default: 0.2 }
    },

    vertexShader: `
                      varying vec2 vUv;
                      
                      void main() {
                                vUv = uv;
                                gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.5);
                      }
            `,

    fragmentShader: `
                      varying vec2 vUv;
                      uniform vec3 color;
                      uniform float timeMsec;

                      void main() {
                                float time = timeMsec / 20000.0;
                                float c = 1.0;
                                float inten = 0.005;

                                vec2 p = mod(vUv * 6.28318530718, 6.28318530718) - 250.0;
                                vec2 i = vec2(p);

                                for (int n = 0; n < 5; n++) {
                                float t = time * (1.0 - (3.5 / float(n + 1)));
                                i = p + vec2(cos(t - i.x) + sin(t + i.y), sin(t - i.y) + cos(t + i.x));
                                c += 1.0 / length(vec2(p.x / (sin(i.x + t) / inten), p.y / (cos(i.y + t) / inten)));
                                }
                                c /= 5.0;
                                c = 1.17 - pow(c, 1.4);
                                vec3 colour = vec3(pow(abs(c), 8.0));
                                colour = clamp(colour + vec3(0.0, 0.35, 0.5), 0.0, 1.0);
                                
                                gl_FragColor = vec4(colour, 1.0);
                      }
            `
});