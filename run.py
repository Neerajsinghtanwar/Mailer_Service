from app.app import app

if __name__ == '__main__':
    # print('neeraj')
    # with app.app_context():
    #     for rule in app.url_map.iter_rules():
    #         print(rule)
    app.run(debug=True)

