import type { Security } from '$db/schema';

export const exportCsv = (data: Security[]) => {
    let headerKeys = [
        "Symbol", 
        "Name", 
        "Sector", 
        "Exchange Currency", 
        "Price", 
        "Price - Updated Date", 
        "Financials - Updated Date", 
        "Financials - Currency", 
        "Financials - Date",
        "Financials - Income",
        "Financials - Shares",
        "Financials - Assets",
        "Financials - Liabilities",
        "Financials - Book Value",
    ];

    let columnDelimiter = ",";
    let lineDelimiter = "\n";
    let result = "";
    result += headerKeys.join(columnDelimiter);
    result += lineDelimiter;
    data.forEach((security) => {
        security.financials.financials.forEach((row) => {
            result += security.symbol + columnDelimiter;
            result += security.name + columnDelimiter;
            result += security.sector + columnDelimiter;
            result += security.exchange_currency + columnDelimiter;
            result += security.price.price + columnDelimiter;
            result += security.price.date + columnDelimiter;
            result += security.financials.date + columnDelimiter;
            result += security.financials.currency + columnDelimiter;
            result += row.date + columnDelimiter;
            result += row.income_statement.income + columnDelimiter;
            result += row.income_statement.shares + columnDelimiter;
            result += row.balance_sheet.assets + columnDelimiter;
            result += row.balance_sheet.liabilities + columnDelimiter;
            result += row.balance_sheet.book_value;
            result += lineDelimiter;
        });
    });

    // create a download link and click it
    var blob = new Blob([result]);
    let link = document.createElement("a");
        if (link.download !== undefined) {
            // Browsers that support HTML5 download attribute
            var url = URL.createObjectURL(blob);
            link.setAttribute("href", url);
            link.setAttribute("download", `export-${(new Date()).toISOString().substring(0, 10)}.csv`);
            link.style.visibility = "hidden";
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }
};
