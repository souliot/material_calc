import { PageContainer, ProCard, ProForm, ProFormUploadButton } from '@ant-design/pro-components';
import { useIntl, useModel } from '@umijs/max';
import { Button, Image } from 'antd';
import React from 'react';

import { download, hkl, img } from '@/services/ela';
import { MsgGetError } from '@/utils/msg';

const ElaVision: React.FC = () => {
  /**
   * @en-US International configuration
   * @zh-CN 国际化配置
   * */
  const intl = useIntl();

  const { calcRes, setCalcRes, curDir, setCurDir, downloadLoading, setDownloadLoading } =
    useModel('ela_vision');
  const { dataForm } = useModel('ela');

  const resColumns = [
    {
      title: 'img',
      key: 'img',
      dataIndex: 'img',
      valueType: 'image',
      copyable: true,
    },
  ];

  const onCalcElaHkl = async (values: any) => {
    const data = new FormData();
    data.append('poscar', values.poscar[0].originFileObj);
    data.append('outcar', values.outcar[0].originFileObj);
    data.append('clear', 'false');
    if (curDir) {
      data.set('dir', curDir);
    }
    const res = await hkl(data);
    if (res.code != 1) {
      MsgGetError('可视化', '二维极坐标投影');
      return;
    }
    setCurDir(res?.data?.workDir);

    data.set('dir', res?.data?.workDir);
    const imgData = await img(data);
    // console.log(imgData);

    var blob = new Blob([imgData]);
    //新窗口打开
    const imgUrl = URL.createObjectURL(blob);
    setCalcRes({
      img: imgUrl,
    });
  };

  const onCalcElaDownload = async (values: any) => {
    const data = new FormData();
    data.append('poscar', values.poscar[0].originFileObj);
    data.append('outcar', values.outcar[0].originFileObj);
    data.append('clear', 'false');
    if (curDir) {
      data.set('dir', curDir);
    }

    const zipData = await download(data);
    var blob = new Blob([zipData], {
      type: 'application/zip',
    });
    //新窗口打开
    let link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.target = '_blank';
    link.download = 'ela_calc.zip';
    await link.click();
  };

  return (
    <PageContainer
      header={{
        breadcrumb: {},
      }}
    >
      <ProForm
        form={dataForm}
        submitter={{
          searchConfig: {
            submitText: intl.formatMessage({
              id: 'pages.ela.vision',
              defaultMessage: 'Material Calc',
            }),
          },
          render: ({ form }, doms) => {
            return [
              ...doms,
              <Button
                type="primary"
                loading={downloadLoading}
                onClick={async () => {
                  setDownloadLoading(true);
                  await onCalcElaDownload(form?.getFieldsValue());
                  setDownloadLoading(false);
                }}
                key="elatools"
              >
                {intl.formatMessage({
                  id: 'pages.ela.vision.download',
                  defaultMessage: 'Material Calc',
                })}
              </Button>,
            ];
          },
        }}
        onFinish={async (values) => {
          await onCalcElaHkl(values);
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
            onChange: () => {
              setCurDir('');
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
            onChange: () => {
              setCurDir('');
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
        <Image
          src={calcRes?.img}
          fallback="data:image/png;base64,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"
        />
      </ProCard>
    </PageContainer>
  );
};

export default ElaVision;
