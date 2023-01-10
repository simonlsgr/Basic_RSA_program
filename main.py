import flask
import rsa as rsa

app = flask.Flask(__name__)



@app.route("/", methods=["GET", "POST"])
def main():
    
    # global key
    output_encrypt_ciphertext = ""
    output_encrypt_key = ""
    output_decrypt = ""
    
    if flask.request.method == "POST":
        message_input =  flask.request.form.getlist("message")
        
        Ciphertext_input = flask.request.form.getlist("Ciphertext")
        key_input = flask.request.form.getlist("key")
        
        
        if message_input:
            key = rsa.rsa().generate_key(200, 210)
            message_input = message_input[0]
            message_numbers_list = []
            for i in message_input:
                message_numbers_list.append(ord(i))
            encrypted_message = rsa.rsa().encrypt(message_numbers_list, key)
            output_encrypt_ciphertext = "Ciphertext: " + str(encrypted_message) + ""
            output_encrypt_key = "Key: " + str(key) + ""
                
        elif Ciphertext_input:
            
            Ciphertext_input = eval(Ciphertext_input[0])
            key_input = eval(key_input[0])
            decrypted_message = rsa.rsa().decrypt(Ciphertext_input, key_input)
            decrypted_message_out = []
            for i in decrypted_message:
                decrypted_message_out.append(chr(i))
            decrypted_message_out = "".join(decrypted_message_out)
            output_decrypt = "<p>Decrypted message: " + decrypted_message_out + "</p>"
            
            
    
    
    html = f"""
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <link rel="stylesheet" href="/static/css/index.css" />
    <title>RSA</title>
</head>

<body>
    <main>
        <div class="container">
            <div class="header">
                <h1>Encrypt</h1>
            </div>
            <div class="content">
                <form action="/" method="POST">
                    <div class="input">
                        <input type="text" required name="message" id="message" placeholder="Message…" />
                    </div>
                    <div class="input">
                        <input class="button" type="submit" value="Encrypt" />
                    </div>
                </form>
                <div class="output">
                    <p>{output_encrypt_ciphertext}</p>
                    <p>{output_encrypt_key}</p>
                </div>
            </div>
        </div>
        <div class="container">

            <div class="header">
                <h1>Decrypt</h1>
            </div>
            <div class="content">
                <form action="/" method="POST">
                    <div class="input">
                        <input type="text" required name="Ciphertext" id="Ciphertext" placeholder="Ciphertext…" />
                        <input type="text" required name="key" id="key" placeholder="Key…" />
                    </div>
                    <div class="input">
                        <input class="button" type="submit" value="Decrypt" />
                    </div>
                </form>
                <div class="output">
                    {output_decrypt}
                </div>
            </div>
        </div>
    </main>
</body>

</html>
    """
    return html


if __name__ == "__main__":
    app.run(debug=True)