from imgurpython import ImgurClient

client_id = 'f87e8dea34b801d'
client_secret = 'b31642a01470a588d71927bc52a3ce9d035baa08'
access_token = '5b6974a8f64edd1ebfc388dfa927d9eb5c98d9f0'
refresh_token = '987cdc7f81bcbc406e4892e4533ca0ffceb092cd'
def upload_photo(image_path):
    
    client = ImgurClient(client_id, client_secret, access_token, refresh_token)
    album = 'oTOC0' # You can also enter an album ID here
    config = {
		'album': album,
	}

    print("Uploading image... ")
    image = client.upload_from_path(image_path, config=config, anon=False)
    print("Done")    
    return image['link']
