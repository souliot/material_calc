// @ts-ignore
// @eslint-disable
import { request } from '@umijs/max';

import { BasicApiResponse } from '@/types/basic';

const BASIC_PATH = '/api/v1/vasp/validate';

export async function all(data: any) {
  const res = await request<BasicApiResponse<any>>(`${BASIC_PATH}`, {
    method: 'POST',
    data,
  });
  return res as BasicApiResponse<any>;
}

export async function cij(data: any) {
  const res = await request<BasicApiResponse<any>>(`${BASIC_PATH}/cij`, {
    method: 'POST',
    data,
  });
  return res as BasicApiResponse<any>;
}

export async function di(data: any) {
  const res = await request<BasicApiResponse<any>>(`${BASIC_PATH}/di`, {
    method: 'POST',
    data,
  });
  return res as BasicApiResponse<any>;
}

export async function piezo(data: any) {
  const res = await request<BasicApiResponse<any>>(`${BASIC_PATH}/piezo`, {
    method: 'POST',
    data,
  });
  return res as BasicApiResponse<any>;
}
