import { Form } from 'antd';

export default function ElaCalc() {
  const [dataForm] = Form.useForm();

  return {
    dataForm,
  };
}
