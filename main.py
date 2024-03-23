import datetime
import json
import os

from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader("./templates"))
data = {"images": []}


def generate_tag_notext(images):
    c = 0
    imgs_tag = []
    for image in images:
        # image["url"] = "https://picsum.photos/286/180"
        imgs_tag.append(f"""
        <div class="col enter-block">
            <ul class="img_content">
                <div class="card" style="width: 18rem;">
                    <a href="{image['url']}" data-lightbox="group"><img src="{image['url']}" width="286px" height="180px"
                        class="thumbnail_js card-image-top" data-image="{image['url']}"></a>
                    <div class="card-body">
                        <p>撮影日: {image['metadata']['created_at']}</p>
                        <a href="{image['metadata']['world']}" class="btn btn-primary">ワールド</a>
                        <a href="{image['metadata']['view_at_url']}" class="btn btn-primary">Misskey.ioで閲覧</a>
                    </div>
                </div>
            </ul>
        </div>""")
        if c >= 3:
            imgs_tag.append('<div class="w-100"></div>')
    return "\n".join(imgs_tag)

def generate_tag(images):
    c = 0
    imgs_tag = []
    for image in images:
        imgs_tag.append(f"""
        <div class="col">
            <ul class="img_content">
                <div class="card" style="width: 18rem;">
                    <a href="{image['url']}" data-lightbox="group"><img src="{image['url']}" width="286px" height="180px"
                        class="thumbnail_js card-image-top" data-image="{image['url']}"></a>
                    <div class="card-body">
                        <p class="card-text">{image['text']}</p>
                        <p>撮影日: {image['metadata']['created_at']}</p>
                        <a href="{image['metadata']['world']}" class="btn btn-primary">ワールド</a>
                        <a href="{image['metadata']['view_at_url']}" class="btn btn-primary">Misskey.ioで閲覧</a>
                    </div>
                </div>
            </ul>
        </div>""")
        if c >= 3:
            imgs_tag.append('<div class="w-100"></div>')
    return "\n".join(imgs_tag)


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
                if sfile["text"] is None:
                    template = env.get_template("index_notext.html")
                    data["images"].append(
                        {
                            "url": src_url,
                            "metadata": {
                                "created_at": d,
                                "world": sfile["metadata"]["world"],
                                "view_at_url": sfile["metadata"]["view_at_url"],
                            },
                            "generate_tag_notext": generate_tag_notext,
                        }
                    )
                    rendered = template.render(
                        data, generate_tag_notext=generate_tag_notext
                    )

                else:
                    template = env.get_template("index.html")
                    data["images"].append(
                        {
                            "url": src_url,
                            "text": sfile["text"].replace("\n", "<br>"),
                            "metadata": {
                                "created_at": d,
                                "world": sfile["metadata"]["world"],
                                "view_at_url": sfile["metadata"]["view_at_url"],
                            },
                            "generate_tag": generate_tag,
                        }
                    )
                    rendered = template.render(data, generate_tag=generate_tag)

with open("./_site/index.html", "w", encoding="utf-8") as f:
    f.write(str(rendered))
