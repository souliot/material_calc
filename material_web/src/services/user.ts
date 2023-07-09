// @ts-ignore
// @eslint-disable
import { request } from '@umijs/max';

import { BasicApiResponse } from '@/types/basic';

const BASIC_PATH = '/api/v1/user';

export async function currentUser(params: any) {
  const res = await request<BasicApiResponse<any>>(`${BASIC_PATH}`, {
    method: 'GET',
    params,
  });
  return res as BasicApiResponse<any>;
}
