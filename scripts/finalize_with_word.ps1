# Mở báo cáo bằng Microsoft Word để cập nhật mục lục tự động, đếm số trang thật
# và xuất bản PDF dùng cho việc kiểm tra bố cục từng trang.

param(
    [string]$ReportPath = "D:\nghialc-portfolio\public\car-valuation-kbdss\outputs\Bao-cao-BTL-Cong-nghe-tri-thuc.docx",
    [string]$PdfPath    = "D:\nghialc-portfolio\public\car-valuation-kbdss\outputs\Bao-cao-BTL-Cong-nghe-tri-thuc.pdf"
)

$ErrorActionPreference = "Stop"

$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0

try {
    $document = $word.Documents.Open($ReportPath, $false, $false)

    # Cập nhật toàn bộ trường, trong đó có trường mục lục tự động.
    foreach ($tableOfContents in $document.TablesOfContents) {
        $tableOfContents.Update()
    }
    $document.Fields.Update() | Out-Null

    # Thống kê số trang và số từ sau khi Word đã phân trang thật.
    $wdStatisticPages = 2
    $wdStatisticWords = 0
    $pageCount = $document.ComputeStatistics($wdStatisticPages, $false)
    $wordCount = $document.ComputeStatistics($wdStatisticWords, $false)

    Write-Output "So trang: $pageCount"
    Write-Output "So tu:    $wordCount"

    $document.Save()

    $wdExportFormatPDF = 17
    $document.ExportAsFixedFormat($PdfPath, $wdExportFormatPDF)
    Write-Output "Da xuat PDF: $PdfPath"

    $document.Close($false)
}
finally {
    $word.Quit()
    [System.Runtime.InteropServices.Marshal]::ReleaseComObject($word) | Out-Null
}
