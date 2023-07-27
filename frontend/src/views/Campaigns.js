import { useEffect } from "react";
import {
  AiOutlineCloseSquare,
  AiOutlineCheckSquare,
  AiFillCheckSquare,
} from "react-icons/ai";
import { useState } from "react";
import { Table, Divider, Card } from "antd";
import { Header } from "../compononents/Header";
import { getCampaigns, getLineItems } from "../services/PlacementsInvoiceAPI";
import { toUSD, toEUR } from "../utils";
import { AdjustmentsValueOrInput } from "../compononents/AdjustmentsValueOrInput";
import { patchLineItem } from "../services/PlacementsInvoiceAPI";

export function Campaigns() {
  const [showInvoice, setShowInvoice] = useState(false);
  const [selectedCampaign, setSelectedCampaign] = useState(undefined);
  const [campaigns, setCampaigns] = useState(undefined);
  const [lineItems, setLineItems] = useState(undefined);

  useEffect(() => {
    const fetchCampaigns = async () => {
      const eventData = await getCampaigns();
      setCampaigns(eventData.data);
    };
    fetchCampaigns();
  }, []);

  const fetchLineItems = async (campaignId) => {
    const eventData = await getLineItems({
      campaign_id: campaignId,
    });
    setLineItems(eventData.data);
  };

  const editLineItem = async ({ lineItemId, lineItemEditPayload }) => {
    await patchLineItem({
      lineItemId,
      lineItemEditPayload,
    });
  };

  const columns = [
    {
      title: "ID",
      dataIndex: "id",
      key: "id",
    },
    {
      title: "Name",
      dataIndex: "name",
      key: "name",
      render: (_, record) => (
        <span
          onClick={() => {
            setSelectedCampaign(record);
            fetchLineItems(record.id);
            setShowInvoice(true);
          }}
          className="hover:underline font-bold hover:cursor-pointer"
        >
          {record.name}
        </span>
      ),
    },
  ];

  const lineItemColumns = [
    {
      title: "ID",
      dataIndex: "id",
      key: "id",
      sorter: (a, b) => a.id - b.id,
      defaultSortOrder: "ascend",
    },
    {
      title: "Name",
      dataIndex: "name",
      key: "name",
    },
    {
      title: "Booked Amount",
      dataIndex: "booked_amount",
      key: "booked_amount",
      render: (text) => <span title={text}>{toUSD(text)}</span>,
    },
    {
      title: "Actual Amount",
      dataIndex: "actual_amount",
      key: "actual_amount",
      render: (text) => <span title={text}>{toUSD(text)}</span>,
    },
    {
      title: "Adjustments",
      dataIndex: "adjustments",
      key: "adjustments",
      render: (text, record) => (
        <AdjustmentsValueOrInput
          lineItemId={record.id}
          value={text}
          onValueUpdate={() => {
            fetchLineItems(record.campaign.id);
          }}
        />
      ),
    },
    {
      title: "Billable Amount (USD)",
      dataIndex: "billable_amount",
      key: "billable_amount",
      render: (text) => <span title={text}>{toUSD(text)}</span>,
      sorter: (a, b) => a.billable_amount - b.billable_amount,
    },
    {
      title: "Billable Amount (Euro)",
      dataIndex: "billable_amount_euro",
      key: "billable_amount_euro",
      render: (text) => <span title={text}>{toEUR(text)}</span>,
      sorter: (a, b) => a.billable_amount - b.billable_amount,
    },
    {
      title: "Reviewed",
      key: "reviewed",
      render: (_, record) => {
        return (
          <span
            onClick={() => {
              editLineItem({
                lineItemId: record.id,
                lineItemEditPayload: { is_reviewed: !record.is_reviewed },
              });
              fetchLineItems(record.campaign.id);
            }}
          >
            {record.is_reviewed ? (
              <AiFillCheckSquare />
            ) : (
              <AiOutlineCheckSquare />
            )}
          </span>
        );
      },
    },
  ];

  const invoice = (
    <div className="relative flex h-full w-auto flex-col  bg-white p-4">
      <div
        onClick={() => {
          setShowInvoice((prevValue) => {
            return !prevValue;
          });
        }}
      >
        <div className="flex flex-row place-items-center mb-6 gap-1">
          <AiOutlineCloseSquare />{" "}
          <span className="font-black">Close Invoice</span>
        </div>
      </div>

      <div>
        {lineItems && (
          <>
            <h2 className="font-black mb-3">{selectedCampaign.name}</h2>
            <h2 className="font-bold mb-3 p-2">
              <Card title="Invoice Total" bordered style={{ width: 300 }}>
                {selectedCampaign.total_billable_amount &&
                  toUSD(selectedCampaign.total_billable_amount)}
              </Card>
            </h2>
            <Divider plain>Line Items</Divider>
            <span>
              *Values shown are rounded up to the nearest cent. Hover for actual
              the value.
            </span>
            <Table columns={lineItemColumns} dataSource={lineItems} />
          </>
        )}
      </div>
    </div>
  );

  return (
    <div className="flex h-full flex-col gap-2">
      <Header />
      <Table columns={columns} dataSource={campaigns} />
      {showInvoice && invoice}
    </div>
  );
}
