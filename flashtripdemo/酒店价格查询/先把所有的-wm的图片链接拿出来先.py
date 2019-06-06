with open('/Users/huangjack/PycharmProjects/codeformyself/flashtripdemo/酒店价格查询/酒店详情页.html', 'r') as f:
    text = f.read()
import re

result_list = re.findall('https:\/\/.*?jpg', text)
# if 'photo-w' or 'photo-m' in

filter_result = set([result for result in result_list if 'photo-w' in result or 'photo-m' in result])
print(filter_result)

print(
    {'https://ccm.ddcdn.com/ext/photo-w/0f/8f/2c/91/park-grand-london-kensington.jpg',
     'https://ccm.ddcdn.com/photo-m/1280/17/3c/28/ba/scenic05757477575.jpg',
     'https://ccm.ddcdn.com/ext/photo-w/0f/8f/2d/80/park-grand-london-kensington.jpg',
     'https://ccm.ddcdn.com/ext/photo-w/0f/8f/2c/eb/park-grand-london-kensington.jpg',
     'https://ccm.ddcdn.com/ext/photo-w/11/6f/f4/b9/afternoon-tea-at-park.jpg',
     'https://ccm.ddcdn.com/ext/photo-w/0f/8f/2b/74/park-grand-london-kensington.jpg',
     'https://ccm.ddcdn.com/ext/photo-w/11/6f/f6/e4/indian-afternoon-tea.jpg',
     'https://ccm.ddcdn.com/ext/photo-w/0f/8f/2c/b3/park-grand-london-kensington.jpg',
     'https://ccm.ddcdn.com/ext/photo-w/0f/8f/2d/78/park-grand-london-kensington.jpg',
     'https://ccm.ddcdn.com/ext/photo-w/0f/8f/2b/6d/park-grand-london-kensington.jpg',
     'https://ccm.ddcdn.com/ext/photo-w/0f/8f/2b/3b/park-grand-london-kensington.jpg',
     'https://ccm.ddcdn.com/ext/photo-w/0f/8f/2b/4e/park-grand-london-kensington.jpg',
     'https://ccm.ddcdn.com/photo-w/17/3c/28/ba/scenic05757477575.jpg',
     'https://ccm.ddcdn.com/ext/photo-w/11/6f/f6/1c/indian-afternoon-tea.jpg',
     'https://ccm.ddcdn.com/ext/photo-w/0f/8f/2c/a0/park-grand-london-kensington.jpg',
     'https://ccm.ddcdn.com/ext/photo-w/0f/8f/2b/2b/park-grand-london-kensington.jpg',
     'https://ccm.ddcdn.com/ext/photo-w/11/6f/f6/72/indian-afternoon-tea.jpg',
     'https://ccm.ddcdn.com/ext/photo-w/0f/8f/2b/09/park-grand-london-kensington.jpg',
     'https://ccm.ddcdn.com/ext/photo-w/0f/8f/2b/67/park-grand-london-kensington.jpg'})
