// Alpine Valley — single-pass Shadertoy shader, no textures.
// Raymarched fbm heightfield (derivative-damped "eroded" fbm), a winding river
// carved into a U-shaped valley, snow above the tree line, soft shadows,
// height-based aerial perspective, sun glints on flowing water,
// slow camera dolly along the river driven by iTime.

#define SUN normalize(vec3(0.55, 0.24, 0.80))
#define TMAX 420.0
#define MAXH 95.0

const mat2 M2 = mat2(0.80, 0.60, -0.60, 0.80);

float hash12(vec2 p)
{
    vec3 p3 = fract(vec3(p.xyx) * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return fract((p3.x + p3.y) * p3.z);
}

// value noise with analytic derivatives, returns (n, dn/dx, dn/dy), n in [0,1]
vec3 noised(vec2 x)
{
    vec2 i = floor(x);
    vec2 f = fract(x);
    vec2 u  = f * f * f * (f * (f * 6.0 - 15.0) + 10.0);
    vec2 du = 30.0 * f * f * (f * (f - 2.0) + 1.0);
    float a = hash12(i);
    float b = hash12(i + vec2(1.0, 0.0));
    float c = hash12(i + vec2(0.0, 1.0));
    float d = hash12(i + vec2(1.0, 1.0));
    float k1 = b - a, k2 = c - a, k4 = a - b - c + d;
    return vec3(a + k1 * u.x + k2 * u.y + k4 * u.x * u.y,
                du * vec2(k1 + k4 * u.y, k2 + k4 * u.x));
}

// river centre line (x as a function of z)
float riverX(float z)
{
    return 7.0 * sin(z * 0.021) + 3.0 * sin(z * 0.057 + 1.7);
}

// eroded fbm: octaves are damped where the slope accumulated so far is high
float mountains(vec2 p, int oct)
{
    vec2 q = p * 0.011;
    float a = 0.0, b = 1.0;
    vec2 d = vec2(0.0);
    for (int i = 0; i < 12; i++)
    {
        if (i >= oct) break;
        vec3 n = noised(q);
        n = vec3(n.x * 2.0 - 1.0, n.yz * 2.0);
        d += n.yz;
        a += b * n.x / (1.0 + dot(d, d));
        b *= 0.5;
        q = M2 * q * 2.03;
    }
    return a;
}

float softplus(float x, float k) { return k * log(1.0 + exp(x / k)); }

float terrain(vec2 p, int oct)
{
    float adx = abs(p.x - riverX(p.y));
    float m = mountains(p, oct);
    // valley floor: river bed below water level (y = 0), gentle banks
    float floorH = -1.2 + 2.2 * smoothstep(1.5, 7.0, adx);
    floorH += 0.8 * m * smoothstep(3.0, 12.0, adx);
    // mountains rise away from the river (U-shaped glacial valley)
    float v = smoothstep(4.0, 48.0, adx);
    float hm = softplus(30.0 + 42.0 * m, 5.0);
    return floorH + v * hm;
}

float raymarch(vec3 ro, vec3 rd, float tmax, int oct, int steps)
{
    float t = 0.5, tp = 0.5;
    for (int i = 0; i < 400; i++)
    {
        if (i >= steps) break;
        vec3 p = ro + rd * t;
        float h = p.y - terrain(p.xz, oct);
        if (h < 0.0015 * t)
        {
            // refine between previous and current t
            float a = tp, b = t;
            for (int j = 0; j < 5; j++)
            {
                float c = 0.5 * (a + b);
                vec3 q = ro + rd * c;
                if (q.y - terrain(q.xz, oct) < 0.0) b = c; else a = c;
            }
            return 0.5 * (a + b);
        }
        if (t > tmax || (rd.y > 0.0 && p.y > MAXH)) return -1.0;
        tp = t;
        t += max(0.42 * h, 0.01 + 0.0008 * t);
    }
    return (t < tmax) ? t : -1.0;
}

vec3 calcNormal(vec3 p, float t)
{
    vec2 e = vec2(0.0015 * t + 0.01, 0.0);
    return normalize(vec3(terrain(p.xz - e.xy, 10) - terrain(p.xz + e.xy, 10),
                          2.0 * e.x,
                          terrain(p.xz - e.yx, 10) - terrain(p.xz + e.yx, 10)));
}

float softShadow(vec3 ro, vec3 rd)
{
    float res = 1.0, t = 0.3;
    for (int i = 0; i < 72; i++)
    {
        vec3 p = ro + rd * t;
        float h = p.y - terrain(p.xz, 6);
        res = min(res, 9.0 * h / t);
        if (res < 0.001 || p.y > MAXH) break;
        t += clamp(0.5 * h, 0.3, 14.0);
    }
    res = clamp(res, 0.0, 1.0);
    return res * res * (3.0 - 2.0 * res);
}

float fbm2(vec2 p)
{
    float a = 0.0, b = 0.5;
    for (int i = 0; i < 5; i++)
    {
        a += b * noised(p).x;
        b *= 0.5;
        p = M2 * p * 2.02;
    }
    return a;
}

vec3 skyColor(vec3 rd)
{
    float sd = max(dot(rd, SUN), 0.0);
    float y = max(rd.y, 0.0);
    vec3 col = mix(vec3(0.78, 0.84, 0.92), vec3(0.20, 0.40, 0.76), pow(y, 0.55));
    col += vec3(1.0, 0.70, 0.40) * 0.30 * pow(sd, 5.0);
    col += vec3(1.0, 0.85, 0.60) * 0.60 * pow(sd, 64.0);
    col += vec3(1.0, 0.95, 0.85) * 30.0 * smoothstep(0.9994, 0.9998, sd);
    if (rd.y > 0.0)
    {
        vec2 uv = rd.xz / (rd.y + 0.12) * 1.6 + vec2(iTime * 0.015, iTime * 0.04);
        float c = smoothstep(0.45, 0.80, fbm2(uv));
        vec3 cc = vec3(1.0, 0.97, 0.94) * (0.80 + 0.6 * pow(sd, 4.0));
        col = mix(col, cc, c * 0.65 * smoothstep(0.0, 0.25, rd.y));
    }
    return col;
}

vec3 shadeTerrain(vec3 p, vec3 n, vec3 rd, bool shadows)
{
    float h = p.y;
    float r  = noised(p.xz * 0.15).x;
    float r2 = noised(p.xz * 1.30 + 7.0).x;

    vec3 rock  = mix(vec3(0.19, 0.17, 0.16), vec3(0.34, 0.31, 0.28), r) * (0.80 + 0.40 * r2);
    vec3 grass = mix(vec3(0.09, 0.15, 0.05), vec3(0.20, 0.24, 0.09), r2);
    float g = smoothstep(0.72, 0.90, n.y) * (1.0 - smoothstep(10.0, 20.0, h + 6.0 * r));
    vec3 alb = mix(rock, grass, g);

    // gravel banks next to the water
    float sand = 1.0 - smoothstep(0.25, 1.1, h + 0.5 * r2);
    alb = mix(alb, vec3(0.42, 0.38, 0.32), sand * 0.85);

    // snow: above the snow line on not-too-steep slopes
    float snowLine = 20.0 + 9.0 * (r - 0.5);
    float s = smoothstep(snowLine - 3.0, snowLine + 3.0, h) *
              smoothstep(0.42, 0.68, n.y + 0.15 * (r2 - 0.5));
    alb = mix(alb, vec3(0.92, 0.95, 1.0), s);

    float dif = max(dot(n, SUN), 0.0);
    float sha = (shadows && dif > 0.0) ? softShadow(p + n * 0.1, SUN) : (shadows ? 0.0 : 1.0);
    float amb = 0.5 + 0.5 * n.y;
    float bou = clamp(dot(n, normalize(vec3(-SUN.x, 0.0, -SUN.z))), 0.0, 1.0) * clamp(1.0 - n.y, 0.0, 1.0);

    vec3 lin = vec3(0.0);
    lin += dif * sha * vec3(3.2, 2.85, 2.35);
    lin += amb * vec3(0.38, 0.50, 0.72) * 0.85;
    lin += bou * vec3(0.35, 0.30, 0.25) * 0.5;
    vec3 col = alb * lin;

    vec3 hv = normalize(SUN - rd);
    col += s * sha * dif * pow(max(dot(n, hv), 0.0), 24.0) * vec3(1.0, 0.92, 0.82) * 0.5;
    return col;
}

vec3 aerial(vec3 col, vec3 ro, vec3 rd, float t)
{
    float sd = max(dot(rd, SUN), 0.0);
    const float a = 0.0075, b = 0.032;
    float fogAmt;
    if (abs(rd.y) < 1e-4) fogAmt = a * exp(-ro.y * b) * t;
    else fogAmt = a * exp(-ro.y * b) * (1.0 - exp(-t * rd.y * b)) / (rd.y * b);
    vec3 ext = exp(-fogAmt * vec3(0.55, 0.75, 1.15));
    vec3 fogCol = mix(vec3(0.56, 0.66, 0.82), vec3(1.0, 0.82, 0.60), pow(sd, 6.0));
    return col * ext + fogCol * (1.0 - ext);
}

vec3 waterNormal(vec2 p)
{
    vec2 g = vec2(0.0);
    vec2 q = p * vec2(1.0, 0.45) * 1.6 + vec2(0.0, -iTime * 1.3);
    float a = 0.5;
    for (int i = 0; i < 4; i++)
    {
        g += a * noised(q).yz;
        q = M2 * q * 2.1 + vec2(0.0, -iTime * 0.9);
        a *= 0.55;
    }
    return normalize(vec3(-g.x * 0.16, 1.0, -g.y * 0.08));
}

vec3 shadeWater(vec3 pw, vec3 rd)
{
    vec3 n = waterNormal(pw.xz);
    float depth = max(-terrain(pw.xz, 6), 0.0);

    // refraction: riverbed tinted by depth
    vec3 bed  = vec3(0.30, 0.27, 0.20) * (0.35 + 0.65 * max(SUN.y, 0.0) * 2.0);
    vec3 deep = vec3(0.015, 0.07, 0.085);
    vec3 refr = mix(bed * 0.55, deep, 1.0 - exp(-depth * 1.4));

    // reflection: mountains or sky
    vec3 rr = reflect(rd, n);
    rr.y = abs(rr.y);
    vec3 refl;
    float tr = raymarch(pw + vec3(0.0, 0.05, 0.0), rr, TMAX, 5, 110);
    if (tr > 0.0)
    {
        vec3 rp = pw + rr * tr;
        vec3 rn = calcNormal(rp, tr);
        refl = aerial(shadeTerrain(rp, rn, rr, false), pw, rr, tr);
    }
    else refl = skyColor(rr);

    float fre = 0.02 + 0.98 * pow(1.0 - max(dot(n, -rd), 0.0), 5.0);
    vec3 col = mix(refr, refl, fre);

    float sha = softShadow(pw + vec3(0.0, 0.1, 0.0), SUN);

    // sun glints: a tight lobe on rippled normals plus a broader sheen
    float rs = max(dot(reflect(rd, n), SUN), 0.0);
    col += sha * vec3(1.0, 0.90, 0.70) * (60.0 * pow(rs, 900.0) + 1.2 * pow(rs, 60.0));

    // foam on the shallow edges
    float foam = (1.0 - smoothstep(0.0, 0.18, depth)) *
                 smoothstep(0.5, 0.8, noised(pw.xz * vec2(3.0, 1.0) + vec2(0.0, -iTime * 2.0)).x);
    col = mix(col, vec3(0.85, 0.9, 0.95) * (0.4 + 0.6 * sha), foam * 0.5);
    return col;
}

vec3 aces(vec3 x)
{
    return clamp((x * (2.51 * x + 0.03)) / (x * (2.43 * x + 0.59) + 0.14), 0.0, 1.0);
}

void mainImage(out vec4 fragColor, in vec2 fragCoord)
{
    vec2 uv = (2.0 * fragCoord - iResolution.xy) / iResolution.y;

    // camera: slow dolly following the river
    float z = iTime * 4.0;
    vec3 ro = vec3(riverX(z), 0.0, z);
    ro.y = max(terrain(ro.xz, 5), 0.0) + 6.0 + 1.0 * sin(iTime * 0.15);
    float zt = z + 28.0;
    vec3 ta = vec3(riverX(zt), 3.5, zt);
    if (iMouse.z > 0.0)
    {
        float yaw = (iMouse.x / iResolution.x - 0.5) * 3.0;
        float pit = (iMouse.y / iResolution.y - 0.5) * 1.2;
        vec3 d = ta - ro;
        float c = cos(yaw), s = sin(yaw);
        d.xz = mat2(c, s, -s, c) * d.xz;
        d.y += pit * 28.0;
        ta = ro + d;
    }
    vec3 ww = normalize(ta - ro);
    vec3 uu = normalize(cross(ww, vec3(0.0, 1.0, 0.0)));
    vec3 vv = cross(uu, ww);
    vec3 rd = normalize(uv.x * uu + uv.y * vv + 1.7 * ww);

    float tW = (rd.y < 0.0) ? -ro.y / rd.y : 1e9;
    float tmax = min(TMAX, tW);
    float t = raymarch(ro, rd, tmax, 8, 260);

    vec3 col;
    if (t > 0.0)
    {
        vec3 p = ro + rd * t;
        vec3 n = calcNormal(p, t);
        col = shadeTerrain(p, n, rd, true);
        col = aerial(col, ro, rd, t);
    }
    else if (tW < TMAX)
    {
        vec3 pw = ro + rd * tW;
        col = shadeWater(pw, rd);
        col = aerial(col, ro, rd, tW);
    }
    else
    {
        col = skyColor(rd);
        col = mix(aerial(col, ro, rd, TMAX), col, smoothstep(0.0, 0.25, rd.y));
    }

    // sun glare
    float sd = max(dot(rd, SUN), 0.0);
    col += vec3(1.0, 0.65, 0.35) * 0.12 * pow(sd, 4.0);

    col = aces(col * 0.85);
    col = pow(col, vec3(1.0 / 2.2));
    vec2 q = fragCoord / iResolution.xy;
    col *= 0.6 + 0.4 * pow(16.0 * q.x * q.y * (1.0 - q.x) * (1.0 - q.y), 0.15);
    col += (hash12(fragCoord + fract(iTime)) - 0.5) / 255.0;
    fragColor = vec4(col, 1.0);
}
