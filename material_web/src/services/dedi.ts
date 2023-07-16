// @ts-ignore
// @eslint-disable
import { request } from '@umijs/max';

import { BasicApiResponse } from '@/types/basic';

const BASIC_PATH = '/api/v1/dedi';

export async function dedi(data: any) {
  const res = await request<BasicApiResponse<any>>(`${BASIC_PATH}`, {
    method: 'POST',
    data,
  });
  return res as BasicApiResponse<any>;
}

export async function dij(data: any) {
  const res = await request<BasicApiResponse<any>>(`${BASIC_PATH}/dij`, {
    method: 'POST',
    data,
  });
  return res as BasicApiResponse<any>;
}
