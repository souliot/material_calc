import {
  PageContainer,
  ProCard,
  ProDescriptions,
  ProForm,
  ProFormUploadButton,
} from '@ant-design/pro-components';
import { useIntl, useModel } from '@umijs/max';
import { Button } from 'antd';
import React from 'react';

import { dedi } from '@/services/dedi';

const Calc: React.FC = () => {
  /**
   * @en-US International configuration
   * @zh-CN 国际化配置
   * */
  const intl = useIntl();

  const { calcRes, setCalcRes } = useModel('diele_calc');

  const resColumns = [
    {
      title: 'εij_ele',
      key: 'εij_ele',
      dataIndex: 'εij_ele',
      valueType: 'code',
      copyable: true,
    },
    {
      title: 'εij_ion',
      key: 'εij_ion',
      dataIndex: 'εij_ion',
      valueType: 'code',
      copyable: true,
    },
    {
      title: 'εij_total',
      key: 'εij_total',
      dataIndex: 'εij',
      valueType: 'code',
      copyable: true,
    },
  ];

  const getCalcBtnName = () => {
    return intl.formatMessage({
      id: 'pages.diele.calc',
      defaultMessage: 'Material Calc',
    });
  };

  const onCalcDedi = async (values: any) => {
    setCalcRes({});
    const data = new FormData();
    data.append('outcar_de', values.outcar_de[0].originFileObj);
    data.append('outcar_di', values.outcar_di[0].originFileObj);

    const res = await dedi(data);
    if (res.code != 1) {
      return;
    }
    setCalcRes(res.data);
  };

  return (
    <PageContainer
      header={{
        breadcrumb: {},
      }}
    >
      <ProForm
        submitter={{
          searchConfig: {
            submitText: getCalcBtnName(),
          },
          render: ({ form }, doms) => {
            return [...doms];
          },
        }}
        onFinish={async (values) => {
          await onCalcDedi(values);
        }}
      >
        <ProFormUploadButton
          name="outcar_de"
          label="OUTCAR_ele"
          title="请选择OUTCAR_ele文件"
          max={1}
          fieldProps={{
            beforeUpload: () => {
              return false;
            },
          }}
          rules={[{ required: true, message: '请选择OUTCAR_ele文件!' }]}
        />
        <ProFormUploadButton
          name="outcar_di"
          label="OUTCAR_ion"
          title="请选择OUTCAR_ion文件"
          max={1}
          fieldProps={{
            beforeUpload: () => {
              return false;
            },
          }}
          rules={[{ required: true, message: '请选择OUTCAR_ion文件!' }]}
        />
      </ProForm>
      <ProCard
        title="计算结果"
        subTitle=""
        style={{ marginTop: 20 }}
        bordered
        headerBordered
        extra={
          <Button
            onClick={async () => {
              await setCalcRes({});
            }}
            key="refresh"
          >
            重置
          </Button>
        }
      >
        <ProDescriptions column={1} size={'middle'} dataSource={calcRes} columns={resColumns} />
      </ProCard>
    </PageContainer>
  );
};

export default Calc;
