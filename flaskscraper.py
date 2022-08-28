from flask import Flask, render_template, request, redirect

#modules needed to run the code
import requests
from bs4 import BeautifulSoup

#where jewllery data is stored
ringdata = []
necklacedata = []
earringdata = []
charmsdata = []
braceletdata = []
ankletdata = []

#request Pandora website and generate html
def reqpandora(weburl):

    page = requests.get(weburl)
    soup = BeautifulSoup(page.content, 'html.parser')

    results = soup.find(id='search-result-items')
    products = results.find_all('div', class_='product-tile')

    return(products, soup)

#scrape name, link, price and metal from Pandora
def scrapepandora(tiles, soup, data):
    #Scrapping info for rings
    for t in tiles:

        name = t.find('a', class_ ='product-name js-name-link')
        price = t.find('span', class_ ='price-sales ProdPrice__regularPrice')

        if data == charmsdata:
            metal = 'metal'
        else:
            metal = soup.find('div', {'class': 'MetalVariants__list-item selected'})['data-metalgroup']


        jewellerystring = []
        jewellerystring.append(name.text.strip().lower())
        jewellerystring.append(name.get('href').strip().lower())
        jewellerystring.append(price.text.strip().lower())
        jewellerystring.append(metal.lower())
        data.append(jewellerystring)

#request Claires website and generate html
def reqclaires(weburl):

    page = requests.get(weburl)
    soup = BeautifulSoup(page.content, 'html.parser')


    results = soup.find(id='search-result-items')
    products = results.find_all('div', class_='product-tile')

    return(products, soup)

#scrape name, link, price and metal from Claires
def scrapeclaires(tiles, soup, data):
    #Scrapping info for rings
    for t in tiles:

        details = t.find('a', class_ ='link-wrap')
        detarray = (details.text.strip()).split('\n')


        while("" in detarray) :
            detarray.remove("")

        for i in detarray:
            if len(detarray) < 2:
                detarray.remove(i)
        if detarray == []:
            continue

        detarraystripped = []

        for i in range(2):
            detarraystripped.append(detarray[i].lower())

        detarraystripped.insert(1, (details.get('href').strip()))


        for i in (detarraystripped[0].split()):
            if i == 'Silver':
                detarraystripped.append('silver')
                break
            elif i == 'Gold':
                detarraystripped.append('gold')
                break
            elif i == 'Rose':
                detarraystripped.append('rose gold')
                break
        if len(detarraystripped) < 4:
                detarraystripped.append('metal')

        data.append(detarraystripped)

#request Chanel website and generate html
def reqchanel(weburl):


    page = requests.get(weburl)
    soup = BeautifulSoup(page.content, 'html.parser')

    products = soup.find_all('div', class_='product-grid__item js-product-edito')

    return(products, soup)

#scrape name, link, price and metal from Chanel
def scrapechanel(tiles, soup, data):
    #Scrapping info for rings
    for t in tiles:

        info = t.find('div', class_ ='txt-product')

        infoArray = (info.text.strip()).split('\n')

        price = (infoArray[6]).strip()
        price = price[:-1]

        name = (infoArray[0] + " " + infoArray[1])

        punc = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''

        # Removing punctuations in string
        # Using loop + punctuation string
        for ele in name:
            if ele in punc:
                name = name.replace(ele, "")


        metal = ''

        for i in (infoArray[1].lower()).split():

            if i == 'silver' or i == 'silver,' or i == 'silver.':
                metal = 'Silver'
                break
            elif i == 'gold' or i == 'gold,' or i == 'gold.':
                metal = 'Gold'
                break
            elif i == 'rose' or i == 'pink' or i == 'rose,' or i == 'pink,' or i == 'rose.' or i == 'pink.':
                metal = 'Rose Gold'
                break
        if metal == '':
            metal = 'metal'

        link = ([i['href'] for i in t.find_all('a', href=True)])[0]

        temp = []

        temp.append(name.lower())
        temp.append(link)
        temp.append(price)
        temp.append(metal.lower())
        data.append(temp)
#filter jewellery through key words and output results
def filter(jdata, jewellery, metal, stone, colour):

    #Implementing Synonyms data
    data = []
    #These if statements take fields from the quiz and find synonyms that is more likely to match the jewllery
    if stone == 'diamond':
        data.append('april')
        data.append('sparkling')
        data.append('diamond')
        data.append('diamonds')
    elif stone == 'amethyst':
        data.append('feburary')
        data.append('purple')
        data.append('violet')
        data.append('amethyst')
    elif stone == 'emerald':
        data.append('may')
        data.append('green')
        data.append('emerald')
    elif stone == 'ruby':
        data.append('july')
        data.append('red')
        data.append('ruby')
    elif stone == 'sapphire':
        data.append('september')
        data.append('blue')
        data.append('sapphire')
    else:
        data.append('polished')
        data.append('band')
        data.append('beaded')
        data.append('no stone')
    if colour == 'blue':
        data.append('lapis')
        data.append('ocean')
        data.append('sea')
        data.append('navy')
        data.append('blue')
    elif colour == 'yellow':
        data.append('sun')
        data.append('sunset')
        data.append('yellow')
    elif colour == 'green':
        data.append('nature')
        data.append('green')
    elif colour == 'red':
        data.append('crimson')
        data.append('blood')
        data.append('wine')
        data.append('strawberry')
        data.append('red')
    elif colour == 'pink':
        data.append('pink')
    elif colour == 'white':
        data.append('white')
        data.append('cream')
        data.append('cloud')
        data.append('beige')
    elif colour == 'black':
        data.append('goth')
        data.append('gothic')
        data.append('obsidian')
        data.append('black')
    elif colour == 'purple':
        data.append('magic')
        data.append('purple')
    else:
        data.append('simple')
        data.append('no stone')
    data.append(metal)
    data.append(jewellery)

    #sets results array from final results and res as a temp array
    res = []
    results = []


    #filter through and find elements that match

    #loop through jewllery data
    for i in jdata:
        #loop through words in jewellery name
        for j in i[0].split():
            #loop through synonyms data
            for k in data:
                #if a synonym matches a word in the jewellery name
                if k == j:
                    #appen item to results
                    results.append(i)

    #deletes unique data so only duplicates are left
    #we only want duplicate data as this shows the element has atleast 2 factors in it the user is looking for
    for i in results:

        if i not in res:
            res.append(i)
            results.remove(i)
    res = []

    #makes duplicates unique
    for i in results:
        if i not in res:
            res.append(i)

    results = res


    #If results are empty print error or print results
    if results == []:
        print('nothing found')
    else:
        #output results
        #return results


        return results



#first function that runs
def main(jewellery, price, metal, stone, colour):

    jewel = jewellery

    #if statement that matches store to price range, i.e. Claires = low, Pandora = mid, Chanel = high
    if price == 'high':
        #if statement to scrape correct category of jewellery user has chosen and pass data into the filtewr
        if jewel == 'ring':
            ringtilesch, soup = reqchanel('https://www.chanel.com/gb/fine-jewellery/rings/c/3x1x2/')
            scrapechanel(ringtilesch, soup, ringdata)
            results = filter(ringdata, jewellery, metal, stone, colour)
        elif jewel == 'necklace':
            necklacetilesch, soup = reqchanel('https://www.chanel.com/gb/fine-jewellery/necklaces/c/3x1x1/')
            scrapechanel(necklacetilesch, soup, necklacedata)
            results = filter(necklacedata, jewellery, metal, stone, colour)
        elif jewel == 'earring':
            earringtilesch, soup = reqchanel('https://www.chanel.com/gb/fine-jewellery/earrings/c/3x1x4/')
            scrapechanel(earringtilesch, soup, earringdata)
            results = filter(earringdata, jewellery, metal, stone, colour)
        elif jewel == 'bracelet':
            bracelettilesch, soup = reqchanel('https://www.chanel.com/gb/fine-jewellery/bracelets/c/3x1x3/')
            scrapechanel(bracelettilesch, soup, braceletdata)
            results = filter(braceletdata, jewellery, metal, stone, colour)
        else:
            return None


    elif price == 'mid':

        if jewel == 'ring':
            ringtiles, soup = reqpandora('https://uk.pandora.net/en/jewellery/rings/#position=top&src=categorySearch')
            scrapepandora(ringtiles, soup, ringdata)
            results = filter(ringdata, jewellery, metal, stone, colour)
        elif jewel == 'necklace':
            necklacetiles, soup = reqpandora('https://uk.pandora.net/en/jewellery/necklaces/#position=top&src=categorySearch')
            scrapepandora(necklacetiles, soup, necklacedata)
            results = filter(necklacedata, jewellery, metal, stone, colour)
        elif jewel == 'earring':
            earringtiles, soup = reqpandora('https://uk.pandora.net/en/jewellery/earrings/#position=top&src=categorySearch')
            scrapepandora(earringtiles, soup, earringdata)
            results = filter(earringdata, jewellery, metal, stone, colour)
        elif jewel == 'bracelet':
            charmstiles, soup = reqpandora('https://uk.pandora.net/en/jewellery/charms/#position=top&src=categorySearch')
            scrapepandora(charmstiles, soup, charmsdata)
            bracelettiles, soup = reqpandora('https://uk.pandora.net/en/jewellery/bracelets/#position=top&src=categorySearch')
            scrapepandora(bracelettiles, soup, braceletdata)
            results = filter(charmsdata, jewellery, metal, stone, colour)
            results = filter(braceletdata, jewellery, metal, stone, colour)
        else:
            return None
    elif price == 'low':

        if jewel == 'ring':
            ringtilesc, soup = reqclaires('https://www.claires.com/jewellery/rings/?lang=en_GB')
            scrapeclaires(ringtilesc, soup, ringdata)
            results = filter(ringdata, jewellery, metal, stone, colour)
        elif jewel == 'necklace':
            necklacetilesc, soup = reqclaires('https://www.claires.com/jewellery/necklaces/?lang=en_GB')
            scrapeclaires(necklacetilesc, soup, necklacedata)
            results = filter(necklacedata, jewellery, metal, stone, colour)
        elif jewel == 'earring':
            earringtilesc, soup = reqclaires('https://www.claires.com/jewellery/earrings/?lang=en_GB')
            scrapeclaires(earringtilesc, soup, earringdata)
            results = filter(earringdata, jewellery, metal, stone, colour)
        elif jewel == 'bracelet':
            bracelettilesc, soup = reqclaires('https://www.claires.com/jewellery/bracelets/?lang=en_GB')
            scrapeclaires(bracelettilesc, soup, braceletdata)
            results = filter(braceletdata, jewellery, metal, stone, colour)
        elif jewel == 'anklet':
            anklettilesc, soup = reqclaires('https://www.claires.com/jewellery/anklets/?lang=en_GB')
            scrapeclaires(anklettilesc, soup, ankletdata)
            results = filter(ankletdata, jewellery, metal, stone, colour)
        else:
            return None


    return(results)

price = 'high'
link = ''
if price == 'high':
    link = 'www.chanel.com'
elif price == 'mid':
    link = 'www.pandora.com'
else:
    link = 'www.claires.com'


app = Flask(__name__)

@app.route('/')
def home():
   return render_template('jewellery.html')

@app.route('/jewellery')
def jewellery():
    return render_template('jewellery.html')

@app.route('/form')
def form():
    return render_template('form.html')


@app.route('/res', methods = ['POST', 'GET'])
def res():
    if request.method == 'POST':
        jewellery = request.form.get("jewellery")
        price = request.form.get("price")
        metal = request.form.get("Metal")
        stone = request.form.get("Stone")
        colour = request.form.get("Colour")

        print(colour)

        results = main(jewellery, price, metal, stone, colour)
        return render_template('res.html', results=results, link=link)


if __name__ == "__main__":
   app.run(debug=True, host = '0.0.0.0')
