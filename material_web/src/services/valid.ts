// @ts-ignore
// @eslint-disable
import { request } from '@umijs/max';

import { BasicApiResponse } from '@/types/basic';

const BASIC_PATH = '/api/v1/vasp/validate';

export async function all(data: any) {
  const res = await request<BasicApiResponse<any>>(`${BASIC_PATH}/all`, {
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

export async function εij(data: any) {
  const res = await request<BasicApiResponse<any>>(`${BASIC_PATH}/εij`, {
    method: 'POST',
    data,
  });
  return res as BasicApiResponse<any>;
}

export async function eij(data: any) {
  const res = await request<BasicApiResponse<any>>(`${BASIC_PATH}/eij`, {
    method: 'POST',
    data,
  });
  return res as BasicApiResponse<any>;
}
