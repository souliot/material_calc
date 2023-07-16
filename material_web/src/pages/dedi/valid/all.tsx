import { ProCard, ProForm, ProFormTextArea, ProFormUploadButton } from '@ant-design/pro-components';
import { Result } from 'antd';
import React from 'react';

import { useIntl, useModel } from '@umijs/max';

import { all } from '@/services/valid';

const AllValid: React.FC = () => {
  /**
   * @en-US International configuration
   * @zh-CN 国际化配置
   * */
  const intl = useIntl();

  const { validAllStatus, setAllValidStatus, validAllDetail, setValidAllDetail } =
    useModel('valid');

  const OnValid = async (values: any) => {
    const data = new FormData();
    data.append('cij', values.cij);
    data.append('di', values.di);
    data.append('piezo', values.piezo);
    data.append('poscar', values.poscar[0].originFileObj);

    const res = await all(data);

    if (res.code == 1) {
      setAllValidStatus('success');
      return;
    }
    setAllValidStatus('error');
    setValidAllDetail(res.data);
  };

  return (
    <>
      <ProForm
        submitter={{
          render: (props, doms) => {
            return [...doms];
          },
        }}
        onFinish={async (values) => {
          await OnValid(values);
          return true;
        }}
      >
        <ProFormUploadButton
          extra="目前支持POSCAR文件"
          label="POSCAR"
          name="poscar"
          title="请选择POSCAR文件"
          max={1}
          fieldProps={{
            beforeUpload: () => {
              return false;
            },
          }}
          rules={[{ required: true, message: '请选择POSCAR文件！' }]}
        />
        <ProFormTextArea
          name="di"
          label="Di 矩阵"
          placeholder="请输入Cij矩阵"
          tooltip="3*3 矩阵，空格分割"
          rules={[{ required: true, message: '请输入di矩阵！' }]}
          fieldProps={{
            autoSize: { minRows: 11, maxRows: 20 },
          }}
        />
        <ProFormTextArea
          name="cij"
          label="Cij 矩阵"
          placeholder="请输入Cij矩阵"
          tooltip="6*6 矩阵，空格分割"
          rules={[{ required: true, message: '请输入Cij矩阵！' }]}
          fieldProps={{
            autoSize: { minRows: 11, maxRows: 20 },
          }}
        />
        <ProFormTextArea
          name="piezo"
          label="Piezo 矩阵"
          placeholder="请输入Piezo矩阵"
          tooltip="3*6 矩阵，空格分割"
          rules={[{ required: true, message: '请输入Piezo矩阵！' }]}
          fieldProps={{
            autoSize: { minRows: 11, maxRows: 20 },
          }}
        />
      </ProForm>
      <ProCard title="验证结果" style={{ marginTop: 20 }} bordered headerBordered>
        <Result
          status={validAllStatus}
          title={validAllStatus == 'success' ? '验证成功' : '验证失败'}
          subTitle={validAllDetail}
        />
      </ProCard>
    </>
  );
};

export default AllValid;
