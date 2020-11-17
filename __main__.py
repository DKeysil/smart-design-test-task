from aiohttp import web
from motor_client import SingletonClient
from bson import json_util, objectid
import json

routes = web.RouteTableDef()


@routes.post('/api/create_item')
async def create_item(request: web.Request):
    params = await request.post()
    if not (params.get('title') and params.get('description')):
        return web.json_response({'error': 'title or description is not specified'}, status=422)

    db = SingletonClient.get_data_base()
    result = await db.items.insert_one(dict(params))
    if result:
        return web.json_response({'status': 'ok'}, status=200)


@routes.post('/api/get_items')
async def get_items(request: web.Request):
    params = await request.post()

    db = SingletonClient.get_data_base()
    cursor = db.items.find({})

    if params.get('sort'):
        cursor = cursor.sort(params.get('sort'))

    list_items = await cursor.to_list(length=await db.items.count_documents({}))
    jsn = json_util.dumps({'items': list_items})

    return web.Response(text=jsn, headers={'Content-Type': 'application / json'}, status=200)


@routes.post('/api/get_item')
async def get_item(request: web.Request):
    params = await request.post()

    db = SingletonClient.get_data_base()

    if _id := params.get('_id'):
        _id = json_util.loads(_id)
        if not isinstance(_id, objectid.ObjectId):
            _id = str(_id)

        result = await db.items.find_one({
            '_id': _id
        })

        if not result:
            return web.json_response({'error': 'item not found'}, status=404)

        jsn = json_util.dumps({'item': result})
        return web.Response(text=jsn, headers={'Content-Type': 'application / json'}, status=200)

    return web.json_response({'error': '_id is not specified'}, status=422)

if __name__ == '__main__':
    app = web.Application()
    app.add_routes(routes)
    web.run_app(app)
