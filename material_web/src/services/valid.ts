// @ts-ignore
// @eslint-disable
import { request } from '@umijs/max';

import { BasicApiResponse } from '@/types/basic';

const BASIC_PATH = '/api/v1/vasp/validate';

export async function all(params: any) {
  const res = await request<BasicApiResponse<any>>(`${BASIC_PATH}`, {
    method: 'POST',
    params,
  });
  return res as BasicApiResponse<any>;
}

export async function cij(data: any) {
  const res = await request<BasicApiResponse<any>>(`${BASIC_PATH}/cij`, {
    method: 'POST',
    header: { 'content-type': 'multipart/form-data' },
    data,
  });
  return res as BasicApiResponse<any>;
}

export async function di(params: any) {
  const res = await request<BasicApiResponse<any>>(`${BASIC_PATH}/di`, {
    method: 'POST',
    params,
  });
  return res as BasicApiResponse<any>;
}

export async function piezo(params: any) {
  const res = await request<BasicApiResponse<any>>(`${BASIC_PATH}/piezo`, {
    method: 'POST',
    params,
  });
  return res as BasicApiResponse<any>;
}
