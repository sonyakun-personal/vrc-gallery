import datetime
import json
import os

from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader("./templates"))
data = {"images": []}
if os.path.isfile("./_site/index.html"):
    os.remove("./_site/index.html")
pc = 0
while True:
    if not os.path.exists(f"./_site/{str(pc)}.html"):
        break
    if os.path.isfile(f"./_site/{str(pc)}.html"):
        os.remove(f"./_site/{str(pc)}.html")
        break
    pc = pc + 1


def generate_tag_notext(images):
    c = 0
    imgs_tag = []
    for image in images:
        # image["url"] = "https://picsum.photos/286/180"
        imgs_tag.append(f"""
        <div class="col enter-block">
            <ul class="img_content">
                <div class="card" style="width: 18rem;">
                    <a href="{image['url']}" data-lightbox="group"><img src="{image['pre_url']}" width="286px" height="180px"
                        class="thumbnail_js card-image-top" data-image="{image['pre_url']}"></a>
                    <div class="card-body">
                        <p>撮影日: {image['metadata']['created_at']}</p>
                        <a href="{image['metadata']['world']}" class="btn btn-primary">ワールド</a>
                        <a href="{image['metadata']['view_at_url']}" class="btn btn-primary">Misskey.ioで閲覧</a>
                    </div>
                </div>
            </ul>
        </div>""")
        if c >= 7:
            return "\n".join(imgs_tag)
        else:
            c = c + 1
    return "\n".join(imgs_tag)


def generate_tag(images):
    c = 0
    imgs_tag = []
    for image in images:
        imgs_tag.append(f"""
        <div class="col">
            <ul class="img_content">
                <div class="card" style="width: 18rem;">
                    <a href="{image['url']}" data-lightbox="group"><img src="{image['pre_url']}" width="286px" height="180px"
                        class="thumbnail_js card-image-top" data-image="{image['pre_url']}"></a>
                    <div class="card-body">
                        <p class="card-text">{image['text']}</p>
                        <p>撮影日: {image['metadata']['created_at']}</p>
                        <a href="{image['metadata']['world']}" class="btn btn-primary">ワールド</a>
                        <a href="{image['metadata']['view_at_url']}" class="btn btn-primary">Misskey.ioで閲覧</a>
                    </div>
                </div>
            </ul>
        </div>""")
        if c >= 7:
            return "\n".join(imgs_tag)
        else:
            c = c + 1
    return "\n".join(imgs_tag)


c = 0
for file in os.listdir("./src"):
    if os.path.isfile(os.path.join("./src", file)):
        if file.endswith(".json"):
            with open(os.path.join("./src", file), "r", encoding="utf-8") as f:
                sfile = json.load(f)
                source_file = sfile["source"]["src"]
                with open(sfile["source"]["src"], "rb") as img:
                    created = os.path.getmtime(sfile["source"]["src"])
                    d = datetime.datetime.fromtimestamp(created).strftime(
                        "%Y年%m月%d日 %H時%M分"
                    )
                    if sfile["source"]["name"] == "vrc_image_1":
                        d = "2024年3月11日 4時14分"
                src_url = f"https://github.com/sonyakun-personal/images/blob/master/{sfile["source"]["name"]}.png?raw=true"
                pre_url = src_url
                if sfile["_extra"]["low-quality"]:
                    pre_url = sfile["_extra"]["low-quality"]
                if sfile["text"] is None:
                    template = env.get_template("index_notext.html")
                    data["images"].append(
                        {
                            "url": src_url,
                            "pre_url": pre_url,
                            "metadata": {
                                "created_at": d,
                                "world": sfile["metadata"]["world"],
                                "view_at_url": sfile["metadata"]["view_at_url"],
                            },
                            "generate_tag_notext": generate_tag_notext,
                        }
                    )
                    gt = generate_tag_notext

                else:
                    template = env.get_template("index.html")
                    data["images"].append(
                        {
                            "url": src_url,
                            "pre_url": pre_url,
                            "text": sfile["text"].replace("\n", "<br>"),
                            "metadata": {
                                "created_at": d,
                                "world": sfile["metadata"]["world"],
                                "view_at_url": sfile["metadata"]["view_at_url"],
                            },
                            "generate_tag": generate_tag,
                        }
                    )
                    gt = generate_tag
    if c >= 7:
        rendered = template.render(data, generate_tag=gt)
        if os.path.isfile("./_site/index.html"):
            pc = 0
            while True:
                if not os.path.isfile(f"./_site/{str(pc)}.html"):
                    with open(f"./_site/{str(pc)}.html", "w", encoding="utf-8") as f:
                        f.write(str(rendered))
                        break
                pc = pc + 1
        else:
            with open("./_site/index.html", "w", encoding="utf-8") as f:
                f.write(str(rendered))
        data["page"] = []
        data["images"] = []
        c = 0
    else:
        c = c + 1

rendered = template.render(data, generate_tag=gt)
if os.path.isfile("./_site/index.html"):
    pc = 0
    while True:
        if not os.path.isfile(f"./_site/{str(pc)}.html"):
            with open(f"./_site/{str(pc)}.html", "w", encoding="utf-8") as f:
                f.write(str(rendered))
                break
        pc = pc + 1
else:
    with open("./_site/index.html", "w", encoding="utf-8") as f:
        f.write(str(rendered))
