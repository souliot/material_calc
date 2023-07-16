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

import { ela, hkl } from '@/services/ela';

const ElaValid: React.FC = () => {
  /**
   * @en-US International configuration
   * @zh-CN 国际化配置
   * */
  const intl = useIntl();

  const { calcRes, setCalcRes, hklLoading, setHklLoading } = useModel('ela_calc');

  const resColumns = [
    {
      title: 'Cij',
      key: 'cij',
      dataIndex: 'cij',
      valueType: 'code',
      copyable: true,
    },
    {
      title: 'Sij',
      key: 'sij',
      dataIndex: 'sij',
      valueType: 'code',
      copyable: true,
    },
    {
      title: 'Props',
      key: 'props',
      dataIndex: 'mech_props',
      valueType: 'code',
      copyable: true,
    },
  ];

  const onCalcEla = async (values: any) => {
    setCalcRes({});
    const data = new FormData();
    data.append('poscar', values.poscar[0].originFileObj);
    data.append('outcar', values.outcar[0].originFileObj);

    const res = await ela(data);
    if (res.code != 1) {
      return;
    }
    setCalcRes(res.data);
  };

  const onCalcElaHkl = async (values: any) => {
    const data = new FormData();
    data.append('poscar', values.poscar[0].originFileObj);
    data.append('outcar', values.outcar[0].originFileObj);

    const res = await hkl(data);
    var blob = new Blob([res], {
      type: 'application/zip',
    });
    //新窗口打开
    let link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.target = '_blank';
    link.download = 'ela_calc.zip';
    link.click();
    URL.revokeObjectURL(link.href);
  };

  return (
    <PageContainer
      header={{
        title: intl.formatMessage({
          id: 'menu.ela.calc',
          defaultMessage: 'Material Calc',
        }),
        breadcrumb: {},
      }}
    >
      <ProForm
        submitter={{
          searchConfig: {
            submitText: intl.formatMessage({
              id: 'pages.ela.calc',
              defaultMessage: 'Material Calc',
            }),
          },
          render: ({ form }, doms) => {
            return [
              ...doms,
              <Button
                type="primary"
                loading={hklLoading}
                onClick={async () => {
                  setHklLoading(true);
                  await onCalcElaHkl(form?.getFieldsValue());
                  setHklLoading(false);
                }}
                key="elatools"
              >
                {intl.formatMessage({
                  id: 'pages.ela.calc.hkl',
                  defaultMessage: 'Material Calc',
                })}
              </Button>,
            ];
          },
        }}
        onFinish={async (values) => {
          await onCalcEla(values);
        }}
      >
        <ProFormUploadButton
          name="poscar"
          label="POSCAR"
          title="请选择POSCAR文件"
          extra="目前支持POSCAR文件"
          max={1}
          fieldProps={{
            beforeUpload: () => {
              return false;
            },
          }}
          rules={[{ required: true, message: '请选择POSCAR文件!' }]}
        />
        <ProFormUploadButton
          name="outcar"
          label="OUTCAR"
          title="请选择OUTCAR文件"
          max={1}
          fieldProps={{
            beforeUpload: () => {
              return false;
            },
          }}
          rules={[{ required: true, message: '请选择OUTCAR文件!' }]}
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

export default ElaValid;
