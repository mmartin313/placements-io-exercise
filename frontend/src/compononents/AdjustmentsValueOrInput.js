import { useState } from "react";
import { toUSD } from "../utils";
import { patchLineItem } from "../services/PlacementsInvoiceAPI";
import { message } from "antd";

export function AdjustmentsValueOrInput({ lineItemId, value, onValueUpdate }) {
  const [showValue, setShowValue] = useState(true);
  const [newValue, setNewValue] = useState(value);

  const [messageApi, contextHolder] = message.useMessage();

  const showErrorMsg = (error) => {
    messageApi.open({
      type: "error",
      content: error.response.data.detail,
    });
  };

  const editLineItem = async ({ lineItemEditPayload }) => {
    await patchLineItem({
      lineItemId,
      lineItemEditPayload,
    });
  };

  const component = showValue ? (
    <span
      title={value}
      onClick={() => {
        setShowValue(false);
      }}
    >
      {toUSD(value)}
    </span>
  ) : (
    <input
      type="number"
      value={newValue}
      onChange={(e) => {
        setNewValue(e.target.value);
      }}
      onBlur={async () => {
        try {
          await editLineItem({
            lineItemEditPayload: { adjustments: newValue },
          });
        } catch (error) {
          showErrorMsg(error);
        }

        onValueUpdate();
        setShowValue(true);
      }}
    />
  );

  return (
    <>
      {contextHolder}
      {component}
    </>
  );
}
