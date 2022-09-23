# @title Loading libraries and definitions

import argparse
import math
from pathlib import Path
import sys

sys.path.append('./taming-transformers')

from IPython import display
from omegaconf import OmegaConf
from taming.models import cond_transformer, vqgan
import torch
from torch import nn, optim
from torch.nn import functional as F
from torchvision import transforms
from torchvision.transforms import functional as TF
from tqdm.notebook import tqdm

from CLIP import clip
import kornia.augmentation as K
import numpy as np
import imageio
from PIL import ImageFile, Image
from imgtag import ImgTag  # metadatos
import libxmp  # metadatos
from stegano import lsb
import json
import wget
import urllib.request

ImageFile.LOAD_TRUNCATED_IMAGES = True

# Posibles modelos: ["vqgan_imagenet_f16_16384", "vqgan_imagenet_f16_1024", "wikiart_1024", "wikiart_16384", "coco", "faceshq", "sflckr", "ade20k", "ffhq", "celebahq", "gumbel_8192"]
MODEL = "vqgan_imagenet_f16_16384"


def model_selection():
    imagenet_1024 = False
    imagenet_16384 = True
    gumbel_8192 = False
    coco = False
    faceshq = False
    wikiart_1024 = False
    wikiart_16384 = False
    sflckr = False
    ade20k = False
    ffhq = False
    celebahq = False

    # if imagenet_1024:
    #
    #     !curl - L - o vqgan_imagenet_f16_1024.yaml - C - 'https://heibox.uni-heidelberg.de/d/8088892a516d4e3baf92/files/?p=%2Fconfigs%2Fmodel.yaml&dl=1'  # ImageNet 1024
    #     !curl - L - o vqgan_imagenet_f16_1024.ckpt - C - 'https://heibox.uni-heidelberg.de/d/8088892a516d4e3baf92/files/?p=%2Fckpts%2Flast.ckpt&dl=1'  # ImageNet 1024
    if imagenet_16384:  # ImageNet 16384
        url_yaml = 'https://heibox.uni-heidelberg.de/d/a7530b09fed84f80a887/files/?p=%2Fconfigs%2Fmodel.yaml&dl=1'
        url_ckpt = 'https://heibox.uni-heidelberg.de/d/a7530b09fed84f80a887/files/?p=%2Fckpts%2Flast.ckpt&dl=1'
        urllib.request.urlretrieve(url_yaml,
                                   '/content/drive/MyDrive/CURSO/Proyecto/saturdays-cuentos-code/vqgan_imagenet_f16_16384.yaml')
        urllib.request.urlretrieve(url_ckpt,
                                   '/content/drive/MyDrive/CURSO/Proyecto/saturdays-cuentos-code/vqgan_imagenet_f16_16384.ckpt')

        # !curl - L - o vqgan_imagenet_f16_16384.ckpt - C - 'https://heibox.uni-heidelberg.de/d/a7530b09fed84f80a887/files/?p=%2Fckpts%2Flast.ckpt&dl=1'  # ImageNet 16384
    # if gumbel_8192:
    #     !curl - L - o
    #     gumbel_8192.yaml - C - 'https://heibox.uni-heidelberg.de/d/2e5662443a6b4307b470/files/?p=%2Fconfigs%2Fmodel.yaml&dl=1'  # Gumbel 8192
    #     !curl - L - o
    #     gumbel_8192.ckpt - C - 'https://heibox.uni-heidelberg.de/d/2e5662443a6b4307b470/files/?p=%2Fckpts%2Flast.ckpt&dl=1'  # Gumbel 8192
    # if coco:
    #     !curl - L - o
    #     coco.yaml - C - 'https://dl.nmkd.de/ai/clip/coco/coco.yaml'  # COCO
    #     !curl - L - o
    #     coco.ckpt - C - 'https://dl.nmkd.de/ai/clip/coco/coco.ckpt'  # COCO
    # if faceshq:
    #     !curl - L - o
    #     faceshq.yaml - C - 'https://drive.google.com/uc?export=download&id=1fHwGx_hnBtC8nsq7hesJvs-Klv-P0gzT'  # FacesHQ
    #     !curl - L - o
    #     faceshq.ckpt - C - 'https://app.koofr.net/content/links/a04deec9-0c59-4673-8b37-3d696fe63a5d/files/get/last.ckpt?path=%2F2020-11-13T21-41-45_faceshq_transformer%2Fcheckpoints%2Flast.ckpt'  # FacesHQ
    # if wikiart_1024:
    #     !curl - L - o
    #     wikiart_1024.yaml - C - 'http://mirror.io.community/blob/vqgan/wikiart.yaml'  # WikiArt 1024
    #     !curl - L - o
    #     wikiart_1024.ckpt - C - 'http://mirror.io.community/blob/vqgan/wikiart.ckpt'  # WikiArt 1024
    # if wikiart_16384:
    #     !curl - L - o
    #     wikiart_16384.yaml - C - 'http://eaidata.bmk.sh/data/Wikiart_16384/wikiart_f16_16384_8145600.yaml'  # WikiArt 16384
    #     !curl - L - o
    #     wikiart_16384.ckpt - C - 'http://eaidata.bmk.sh/data/Wikiart_16384/wikiart_f16_16384_8145600.ckpt'  # WikiArt 16384
    # if sflckr:
    #     !curl - L - o
    #     sflckr.yaml - C - 'https://heibox.uni-heidelberg.de/d/73487ab6e5314cb5adba/files/?p=%2Fconfigs%2F2020-11-09T13-31-51-project.yaml&dl=1'  # S-FLCKR
    #     !curl - L - o
    #     sflckr.ckpt - C - 'https://heibox.uni-heidelberg.de/d/73487ab6e5314cb5adba/files/?p=%2Fcheckpoints%2Flast.ckpt&dl=1'  # S-FLCKR
    # if ade20k:
    #     !curl - L - o
    #     ade20k.yaml - C - 'https://static.miraheze.org/intercriaturaswiki/b/bf/Ade20k.txt'  # ADE20K
    #     !curl - L - o
    #     ade20k.ckpt - C - 'https://app.koofr.net/content/links/0f65c2cd-7102-4550-a2bd-07fd383aac9e/files/get/last.ckpt?path=%2F2020-11-20T21-45-44_ade20k_transformer%2Fcheckpoints%2Flast.ckpt'  # ADE20K
    # if ffhq:
    #     !curl - L - o
    #     ffhq.yaml - C - 'https://app.koofr.net/content/links/0fc005bf-3dca-4079-9d40-cdf38d42cd7a/files/get/2021-04-23T18-19-01-project.yaml?path=%2F2021-04-23T18-19-01_ffhq_transformer%2Fconfigs%2F2021-04-23T18-19-01-project.yaml&force'  # FFHQ
    #     !curl - L - o
    #     ffhq.ckpt - C - 'https://app.koofr.net/content/links/0fc005bf-3dca-4079-9d40-cdf38d42cd7a/files/get/last.ckpt?path=%2F2021-04-23T18-19-01_ffhq_transformer%2Fcheckpoints%2Flast.ckpt&force'  # FFHQ
    # if celebahq:
    #     !curl - L - o
    #     celebahq.yaml - C - 'https://app.koofr.net/content/links/6dddf083-40c8-470a-9360-a9dab2a94e96/files/get/2021-04-23T18-11-19-project.yaml?path=%2F2021-04-23T18-11-19_celebahq_transformer%2Fconfigs%2F2021-04-23T18-11-19-project.yaml&force'  # CelebA-HQ
    #     !curl - L - o
    #     celebahq.ckpt - C - 'https://app.koofr.net/content/links/6dddf083-40c8-470a-9360-a9dab2a94e96/files/get/last.ckpt?path=%2F2021-04-23T18-11-19_celebahq_transformer%2Fcheckpoints%2Flast.ckpt&force'  # CelebA-HQ
    return


def sinc(x):
    return torch.where(x != 0, torch.sin(math.pi * x) / (math.pi * x), x.new_ones([]))


def lanczos(x, a):
    cond = torch.logical_and(-a < x, x < a)
    out = torch.where(cond, sinc(x) * sinc(x / a), x.new_zeros([]))
    return out / out.sum()


def ramp(ratio, width):
    n = math.ceil(width / ratio + 1)
    out = torch.empty([n])
    cur = 0
    for i in range(out.shape[0]):
        out[i] = cur
        cur += ratio
    return torch.cat([-out[1:].flip([0]), out])[1:-1]


def resample(input, size, align_corners=True):
    n, c, h, w = input.shape
    dh, dw = size

    input = input.view([n * c, 1, h, w])

    if dh < h:
        kernel_h = lanczos(ramp(dh / h, 2), 2).to(input.device, input.dtype)
        pad_h = (kernel_h.shape[0] - 1) // 2
        input = F.pad(input, (0, 0, pad_h, pad_h), 'reflect')
        input = F.conv2d(input, kernel_h[None, None, :, None])

    if dw < w:
        kernel_w = lanczos(ramp(dw / w, 2), 2).to(input.device, input.dtype)
        pad_w = (kernel_w.shape[0] - 1) // 2
        input = F.pad(input, (pad_w, pad_w, 0, 0), 'reflect')
        input = F.conv2d(input, kernel_w[None, None, None, :])

    input = input.view([n, c, h, w])
    return F.interpolate(input, size, mode='bicubic', align_corners=align_corners)


class ReplaceGrad(torch.autograd.Function):
    @staticmethod
    def forward(ctx, x_forward, x_backward):
        ctx.shape = x_backward.shape
        return x_forward

    @staticmethod
    def backward(ctx, grad_in):
        return None, grad_in.sum_to_size(ctx.shape)


replace_grad = ReplaceGrad.apply


class ClampWithGrad(torch.autograd.Function):
    @staticmethod
    def forward(ctx, input, min, max):
        ctx.min = min
        ctx.max = max
        ctx.save_for_backward(input)
        return input.clamp(min, max)

    @staticmethod
    def backward(ctx, grad_in):
        input, = ctx.saved_tensors
        return grad_in * (grad_in * (input - input.clamp(ctx.min, ctx.max)) >= 0), None, None


clamp_with_grad = ClampWithGrad.apply


def vector_quantize(x, codebook):
    d = x.pow(2).sum(dim=-1, keepdim=True) + codebook.pow(2).sum(dim=1) - 2 * x @ codebook.T
    indices = d.argmin(-1)
    x_q = F.one_hot(indices, codebook.shape[0]).to(d.dtype) @ codebook
    return replace_grad(x_q, x)


class Prompt(nn.Module):
    def __init__(self, embed, weight=1., stop=float('-inf')):
        super().__init__()
        self.register_buffer('embed', embed)
        self.register_buffer('weight', torch.as_tensor(weight))
        self.register_buffer('stop', torch.as_tensor(stop))

    def forward(self, input):
        input_normed = F.normalize(input.unsqueeze(1), dim=2)
        embed_normed = F.normalize(self.embed.unsqueeze(0), dim=2)
        dists = input_normed.sub(embed_normed).norm(dim=2).div(2).arcsin().pow(2).mul(2)
        dists = dists * self.weight.sign()
        return self.weight.abs() * replace_grad(dists, torch.maximum(dists, self.stop)).mean()


def parse_prompt(prompt):
    vals = prompt.rsplit(':', 2)
    vals = vals + ['', '1', '-inf'][len(vals):]
    return vals[0], float(vals[1]), float(vals[2])


class MakeCutouts(nn.Module):
    def __init__(self, cut_size, cutn, cut_pow=1.):
        super().__init__()
        self.cut_size = cut_size
        self.cutn = cutn
        self.cut_pow = cut_pow
        self.augs = nn.Sequential(
            K.RandomHorizontalFlip(p=0.5),
            # K.RandomSolarize(0.01, 0.01, p=0.7),
            K.RandomSharpness(0.3, p=0.4),
            K.RandomAffine(degrees=30, translate=0.1, p=0.8, padding_mode='border'),
            K.RandomPerspective(0.2, p=0.4),
            K.ColorJitter(hue=0.01, saturation=0.01, p=0.7))
        self.noise_fac = 0.1

    def forward(self, input):
        sideY, sideX = input.shape[2:4]
        max_size = min(sideX, sideY)
        min_size = min(sideX, sideY, self.cut_size)
        cutouts = []
        for _ in range(self.cutn):
            size = int(torch.rand([]) ** self.cut_pow * (max_size - min_size) + min_size)
            offsetx = torch.randint(0, sideX - size + 1, ())
            offsety = torch.randint(0, sideY - size + 1, ())
            cutout = input[:, :, offsety:offsety + size, offsetx:offsetx + size]
            cutouts.append(resample(cutout, (self.cut_size, self.cut_size)))
        batch = self.augs(torch.cat(cutouts, dim=0))
        if self.noise_fac:
            facs = batch.new_empty([self.cutn, 1, 1, 1]).uniform_(0, self.noise_fac)
            batch = batch + facs * torch.randn_like(batch)
        return batch


def load_vqgan_model(config_path, checkpoint_path):
    config = OmegaConf.load(config_path)
    if config.model.target == 'taming.models.vqgan.VQModel':
        model = vqgan.VQModel(**config.model.params)
        model.eval().requires_grad_(False)
        model.init_from_ckpt(checkpoint_path)
    elif config.model.target == 'taming.models.cond_transformer.Net2NetTransformer':
        parent_model = cond_transformer.Net2NetTransformer(**config.model.params)
        parent_model.eval().requires_grad_(False)
        parent_model.init_from_ckpt(checkpoint_path)
        model = parent_model.first_stage_model
    elif config.model.target == 'taming.models.vqgan.GumbelVQ':
        model = vqgan.GumbelVQ(**config.model.params)
        print(config.model.params)
        model.eval().requires_grad_(False)
        model.init_from_ckpt(checkpoint_path)
    else:
        raise ValueError(f'unknown model type: {config.model.target}')
    del model.loss
    return model


def resize_image(image, out_size):
    ratio = image.size[0] / image.size[1]
    area = min(image.size[0] * image.size[1], out_size[0] * out_size[1])
    size = round((area * ratio) ** 0.5), round((area / ratio) ** 0.5)
    return image.resize(size, Image.LANCZOS)


def download_img(img_url):
    try:
        return wget.download(img_url, out="input.jpg")
    except:
        return


def get_texts(config_data):
    if len(config_data['parameters']['texts']) > 1:
        texts = '|'.join(config_data['parameters']['texts'])
    else:
        texts = config_data['parameters']['texts'][0]

    texts = [phrase.strip() for phrase in texts.split("|")]
    if texts == ['']:
        texts = []
    return texts


def parameter_definition(config_data):
    texts = get_texts(config_data)
    width = config_data['parameters']['width']
    height = config_data['parameters']['height']

    images_interval = config_data['parameters']['images_interval']
    init_image = config_data['parameters']['init_image']
    target_images = config_data['parameters']['target_images']
    seed = config_data['neural_network']['seed']

    model_names = {"vqgan_imagenet_f16_16384": 'ImageNet 16384', "vqgan_imagenet_f16_1024": "ImageNet 1024",
                   "wikiart_1024": "WikiArt 1024", "wikiart_16384": "WikiArt 16384", "coco": "COCO-Stuff",
                   "faceshq": "FacesHQ", "sflckr": "S-FLCKR", "ade20k": "ADE20K", "ffhq": "FFHQ",
                   "celebahq": "CelebA-HQ", "gumbel_8192": "Gumbel 8192"}
    name_model = model_names[MODEL]

    if MODEL == "gumbel_8192":
        is_gumbel = True
    else:
        is_gumbel = False

    if seed == -1:
        seed = None
    if init_image == "None":
        init_image = None
    elif init_image and init_image.lower().startswith("http"):
        init_image = download_img(init_image)

    if target_images == "None" or not target_images:
        target_images = []
    else:
        target_images = target_images.split("|")
        target_images = [image.strip() for image in target_images]

    args = argparse.Namespace(
        prompts=texts,
        image_prompts=target_images,
        noise_prompt_seeds=[],
        noise_prompt_weights=[],
        size=[width, height],
        init_image=init_image,
        init_weight=0.,
        clip_model='ViT-B/32',
        vqgan_config=f'{MODEL}.yaml',
        vqgan_checkpoint=f'{MODEL}.ckpt',
        step_size=0.1,
        cutn=64,
        cut_pow=1.,
        display_freq=images_interval,
        seed=seed,
        is_gumbel=is_gumbel,
        name_model=name_model,
    )
    return args


def fire_up_ai(args, config_data):
    global i
    texts = args.prompts
    init_image = args.init_image
    target_images = args.image_prompts
    is_gumbel = args.is_gumbel
    name_model = args.name_model
    max_iterations = config_data['parameters']['max_iterations']
    input_images = config_data['parameters']['input_images']

    if init_image or target_images != []:
        input_images = True

    device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
    print('Using device:', device)
    if texts:
        print('Using texts:', texts)
    if target_images:
        print('Using image prompts:', target_images)
    if args.seed is None:
        seed = torch.seed()
    else:
        seed = args.seed
    torch.manual_seed(seed)
    print('Using seed:', seed)

    model = load_vqgan_model(args.vqgan_config, args.vqgan_checkpoint).to(device)
    perceptor = clip.load(args.clip_model, jit=False)[0].eval().requires_grad_(False).to(device)

    cut_size = perceptor.visual.input_resolution
    if is_gumbel:
        e_dim = model.quantize.embedding_dim
    else:
        e_dim = model.quantize.e_dim

    f = 2 ** (model.decoder.num_resolutions - 1)
    make_cutouts = MakeCutouts(cut_size, args.cutn, cut_pow=args.cut_pow)
    if is_gumbel:
        n_toks = model.quantize.n_embed
    else:
        n_toks = model.quantize.n_e

    toksX, toksY = args.size[0] // f, args.size[1] // f
    sideX, sideY = toksX * f, toksY * f
    if is_gumbel:
        z_min = model.quantize.embed.weight.min(dim=0).values[None, :, None, None]
        z_max = model.quantize.embed.weight.max(dim=0).values[None, :, None, None]
    else:
        z_min = model.quantize.embedding.weight.min(dim=0).values[None, :, None, None]
        z_max = model.quantize.embedding.weight.max(dim=0).values[None, :, None, None]

    if args.init_image:
        pil_image = Image.open(args.init_image).convert('RGB')
        pil_image = pil_image.resize((sideX, sideY), Image.LANCZOS)
        z, *_ = model.encode(TF.to_tensor(pil_image).to(device).unsqueeze(0) * 2 - 1)
    else:
        one_hot = F.one_hot(torch.randint(n_toks, [toksY * toksX], device=device), n_toks).float()
        if is_gumbel:
            z = one_hot @ model.quantize.embed.weight
        else:
            z = one_hot @ model.quantize.embedding.weight
        z = z.view([-1, toksY, toksX, e_dim]).permute(0, 3, 1, 2)
    z_orig = z.clone()
    z.requires_grad_(True)
    opt = optim.Adam([z], lr=args.step_size)

    normalize = transforms.Normalize(mean=[0.48145466, 0.4578275, 0.40821073],
                                     std=[0.26862954, 0.26130258, 0.27577711])

    pMs = []

    for prompt in args.prompts:
        txt, weight, stop = parse_prompt(prompt)
        embed = perceptor.encode_text(clip.tokenize(txt).to(device)).float()
        pMs.append(Prompt(embed, weight, stop).to(device))

    for prompt in args.image_prompts:
        path, weight, stop = parse_prompt(prompt)
        img = resize_image(Image.open(path).convert('RGB'), (sideX, sideY))
        batch = make_cutouts(TF.to_tensor(img).unsqueeze(0).to(device))
        embed = perceptor.encode_image(normalize(batch)).float()
        pMs.append(Prompt(embed, weight, stop).to(device))

    for seed, weight in zip(args.noise_prompt_seeds, args.noise_prompt_weights):
        gen = torch.Generator().manual_seed(seed)
        embed = torch.empty([1, perceptor.visual.output_dim]).normal_(generator=gen)
        pMs.append(Prompt(embed, weight).to(device))

    def synth(z):
        if is_gumbel:
            z_q = vector_quantize(z.movedim(1, 3), model.quantize.embed.weight).movedim(3, 1)
        else:
            z_q = vector_quantize(z.movedim(1, 3), model.quantize.embedding.weight).movedim(3, 1)

        return clamp_with_grad(model.decode(z_q).add(1).div(2), 0, 1)

    def add_xmp_data(nombrefichero):
        imagen = ImgTag(filename=nombrefichero)
        imagen.xmp.append_array_item(libxmp.consts.XMP_NS_DC, 'creator', 'VQGAN+CLIP',
                                     {"prop_array_is_ordered": True, "prop_value_is_array": True})
        if args.prompts:
            imagen.xmp.append_array_item(libxmp.consts.XMP_NS_DC, 'title', " | ".join(args.prompts),
                                         {"prop_array_is_ordered": True, "prop_value_is_array": True})
        else:
            imagen.xmp.append_array_item(libxmp.consts.XMP_NS_DC, 'title', 'None',
                                         {"prop_array_is_ordered": True, "prop_value_is_array": True})
        imagen.xmp.append_array_item(libxmp.consts.XMP_NS_DC, 'i', str(i),
                                     {"prop_array_is_ordered": True, "prop_value_is_array": True})
        imagen.xmp.append_array_item(libxmp.consts.XMP_NS_DC, 'model', name_model,
                                     {"prop_array_is_ordered": True, "prop_value_is_array": True})
        imagen.xmp.append_array_item(libxmp.consts.XMP_NS_DC, 'seed', str(seed),
                                     {"prop_array_is_ordered": True, "prop_value_is_array": True})
        imagen.xmp.append_array_item(libxmp.consts.XMP_NS_DC, 'input_images', str(input_images),
                                     {"prop_array_is_ordered": True, "prop_value_is_array": True})
        # for frases in args.prompts:
        #    imagen.xmp.append_array_item(libxmp.consts.XMP_NS_DC, 'Prompt' ,frases, {"prop_array_is_ordered":True, "prop_value_is_array":True})
        imagen.close()

    def add_stegano_data(filename):
        data = {
            "title": " | ".join(args.prompts) if args.prompts else None,
            "notebook": "VQGAN+CLIP",
            "i": i,
            "model": name_model,
            "seed": str(seed),
            "input_images": input_images
        }
        lsb.hide(filename, json.dumps(data)).save(filename)

    @torch.no_grad()
    def checkin(i, losses):
        losses_str = ', '.join(f'{loss.item():g}' for loss in losses)
        tqdm.write(f'i: {i}, loss: {sum(losses).item():g}, losses: {losses_str}')
        out = synth(z)
        TF.to_pil_image(out[0].cpu()).save('progress.png')
        add_stegano_data('progress.png')
        add_xmp_data('progress.png')
        display.display(display.Image('progress.png'))

    def ascend_txt():
        out = synth(z)
        iii = perceptor.encode_image(normalize(make_cutouts(out))).float()

        result = []

        if args.init_weight:
            result.append(F.mse_loss(z, z_orig) * args.init_weight / 2)

        for prompt in pMs:
            result.append(prompt(iii))
        img = np.array(out.mul(255).clamp(0, 255)[0].cpu().detach().numpy().astype(np.uint8))[:, :, :]
        img = np.transpose(img, (1, 2, 0))
        filename = f"steps/{i:04}.png"
        imageio.imwrite(filename, np.array(img))
        add_stegano_data(filename)
        add_xmp_data(filename)
        return result

    def train(i):
        opt.zero_grad()
        lossAll = ascend_txt()
        if i % args.display_freq == 0:
            checkin(i, lossAll)
        loss = sum(lossAll)
        loss.backward()
        opt.step()
        with torch.no_grad():
            z.copy_(z.maximum(z_min).minimum(z_max))

    i = 0
    try:
        with tqdm() as pbar:
            while True:
                train(i)
                if i == max_iterations:
                    break
                i += 1
                pbar.update()
    except KeyboardInterrupt:
        pass


def get_image_by_index(index):
    if index < 10:
        filename = f"steps/000{index}.png"
    elif index < 100:
        filename = f"steps/00{index}.png"
    else:
        filename = f"steps/0{index}.png"
    return filename
