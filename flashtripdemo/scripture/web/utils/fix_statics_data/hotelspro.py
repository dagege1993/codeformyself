# coding: utf-8
import logging
from yarl import URL
import aiohttp
from tasks.supplier_statics import HotelsPro


logger = logging.getLogger(__name__)

class AsyncHotelsPro(HotelsPro):

    async def fetch(self, types, code):
        auth = aiohttp.BasicAuth(self.user, self.token)
        endpoint = self.endpoint / (types + "/" + code)
        async with aiohttp.ClientSession() as sess:
            async with sess.get(
                endpoint,
                auth=auth,
            ) as resp:
                resp = await resp.json()
        if resp:
            return resp[0]
        else:
            return {}
    
    async def hotel(self, codes):
        result = []
        for code in codes:
            ori_doc = await self.fetch('hotels', code)
            if not ori_doc:
                logger.error(f"hotelspro {code} without data!")
                return {}
            doc = self.format_doc(ori_doc)
            logger.info(f"{code} : {doc}")
            self.save(doc)
            if doc:
                logger.info(f"save hotelspro {code} hotel succeed\n")
                result.append(doc)
            else:
                logger.warning(f"unable to save hotelspro {code} hotel")
        return result