import {
  PageContainer,
  ProCard,
  ProDescriptions,
  ProForm,
  ProFormRadio,
  ProFormUploadButton,
} from '@ant-design/pro-components';
import { useIntl, useModel } from '@umijs/max';
import { Button } from 'antd';
import React from 'react';

import { dedi, dij } from '@/services/dedi';

const ElaValid: React.FC = () => {
  /**
   * @en-US International configuration
   * @zh-CN 国际化配置
   * */
  const intl = useIntl();

  const { calcType, setCalcType, calcRes, setCalcRes } = useModel('dedi_calc');

  const resColumns = [
    {
      title: 'Piezo_De',
      key: 'piezo_de',
      dataIndex: 'piezo_de',
      valueType: 'code',
      copyable: true,
    },
    {
      title: 'Piezo_Di',
      key: 'piezo_di',
      dataIndex: 'piezo_di',
      valueType: 'code',
      copyable: true,
    },
    {
      title: 'Piezo_All',
      key: 'piezo_all',
      dataIndex: 'piezo_all',
      valueType: 'code',
      copyable: true,
    },
  ];

  const resDijColumns = [
    {
      title: 'Dij',
      key: 'dij',
      dataIndex: 'dij',
      valueType: 'code',
      copyable: true,
    },
    {
      title: 'Dij_Max',
      key: 'dij_max',
      dataIndex: 'dij_max',
      valueType: 'code',
      copyable: true,
    },
  ];

  const getCalcBtnName = () => {
    return calcType == 'dedi'
      ? intl.formatMessage({
          id: 'pages.dedi.calc',
          defaultMessage: 'Material Calc',
        })
      : intl.formatMessage({
          id: 'pages.dedi.calc.dij',
          defaultMessage: 'Material Calc',
        });
  };

  const onCalcDedi = async (values: any) => {
    setCalcRes({});
    const data = new FormData();
    data.append('outcar_de', values.outcar_de[0].originFileObj);
    data.append('outcar_di', values.outcar_di[0].originFileObj);
    if (calcType == 'dij') {
      data.append('poscar', values.poscar[0].originFileObj);
      data.append('outcar_ela', values.outcar_ela[0].originFileObj);
    }

    if (calcType == 'dij') {
      const res = await dij(data);
      if (res.code != 1) {
        return;
      }
      setCalcRes(res.data);
    } else {
      const res = await dedi(data);
      if (res.code != 1) {
        return;
      }
      setCalcRes(res.data);
    }
  };

  return (
    <PageContainer
      header={{
        title: intl.formatMessage({
          id: 'menu.dedi.calc',
          defaultMessage: 'Material Calc',
        }),
        breadcrumb: {},
      }}
    >
      <ProFormRadio.Group
        style={{
          margin: 16,
        }}
        radioType="button"
        fieldProps={{
          value: calcType,
          onChange: (e) => {
            setCalcType(e.target.value);
          },
        }}
        options={[
          {
            value: 'dedi',
            label: '压电矩阵',
          },
          {
            value: 'dij',
            label: 'Dij 矩阵',
          },
        ]}
      />
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
          label="OUTCAR_DE"
          title="请选择OUTCAR_DE文件"
          max={1}
          fieldProps={{
            beforeUpload: () => {
              return false;
            },
          }}
          rules={[{ required: true, message: '请选择OUTCAR_DE文件!' }]}
        />
        <ProFormUploadButton
          name="outcar_di"
          label="OUTCAR_DI"
          title="请选择OUTCAR_DI文件"
          max={1}
          fieldProps={{
            beforeUpload: () => {
              return false;
            },
          }}
          rules={[{ required: true, message: '请选择OUTCAR_DI文件!' }]}
        />
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
          hidden={calcType == 'dedi'}
          rules={calcType == 'dedi' ? [] : [{ required: true, message: '请选择POSCAR文件!' }]}
        />
        <ProFormUploadButton
          name="outcar_ela"
          label="OUTCAR_ELA"
          title="请选择OUTCAR_ELA文件"
          max={1}
          fieldProps={{
            beforeUpload: () => {
              return false;
            },
          }}
          hidden={calcType == 'dedi'}
          rules={calcType == 'dedi' ? [] : [{ required: true, message: '请选择OUTCAR_ELA文件!' }]}
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
        <ProDescriptions
          column={1}
          size={'middle'}
          dataSource={calcRes}
          columns={calcType == 'dij' ? resColumns.concat(resDijColumns) : resColumns}
        />
      </ProCard>
    </PageContainer>
  );
};

export default ElaValid;
