from flask import Flask, render_template, request, redirect, url_for

from comic_book_generation import create_storyline, create_comic
from io import BytesIO
import base64
app = Flask(__name__)

storyline_comic={}

def pil_to_base64(img):
    img_io = BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)
    base64_img = base64.b64encode(img_io.getvalue()).decode('utf8')
    return f"data:image/png;base64,{base64_img}"

def dict_to_string(response_json):
    final_story=[]
    for idx,i in enumerate(response_json.keys()):
        panel_story="("+str(idx+1)+"): "

        for j in response_json[i].keys():
            panel_story=panel_story+" --- "+j.capitalize()+": "+response_json[i][j]
        
        final_story.append(panel_story)
    return final_story
    
@app.route('/', methods=['GET', 'POST'])
def index():
    global storyline_comic
    if request.method == 'POST':
        user_prompt = request.form['prompt']
        style = request.form['style']
        storyline_comic['user_prompt']=user_prompt
        storyline_comic['style']=style

        # return render_template('index.html', panels='strip.png')
        story_panel = create_storyline(user_prompt, style)
        storyline_comic['story_panel']=story_panel
        final_story=dict_to_string(story_panel)
        storyline_comic['final_story']=final_story

        
        return render_template('index.html', panels=None, story_panel=final_story, prompt=user_prompt, style=style)

    return render_template('index.html', panels=None)

@app.route('/generate_comic', methods=['POST'])
def generate_comic():
    global storyline_comic
    prompt=storyline_comic['user_prompt']
    style=storyline_comic['style']
    story_dict=storyline_comic['story_panel']
    final_story=storyline_comic['final_story']
    
    comic_img = create_comic(story_dict, style)
    comic_img.save("output/strip.png")
    comic_img_url = pil_to_base64(comic_img)
    return render_template('index.html', comic_img_url=comic_img_url, story_panel=final_story, prompt=prompt, style=style)



if __name__ == '__main__':
    app.run(debug=True)
