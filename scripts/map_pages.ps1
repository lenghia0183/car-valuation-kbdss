# Liệt kê số trang bắt đầu của từng tiêu đề cấp 1, để biết phần nào chiếm nhiều trang nhất.

param(
    [string]$ReportPath = "D:\nghialc-portfolio\public\car-valuation-kbdss\outputs\Bao-cao-BTL-Cong-nghe-tri-thuc.docx"
)

$ErrorActionPreference = "Stop"

$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0

try {
    $document = $word.Documents.Open($ReportPath, $false, $true)

    $wdActiveEndPageNumber = 3
    $wdStatisticPages = 2

    foreach ($paragraph in $document.Paragraphs) {
        $styleName = $paragraph.Style.NameLocal

        if ($styleName -like "Heading 1" -or $styleName -like "*u 1") {
            $text = $paragraph.Range.Text.Trim()
            if ($text) {
                $page = $paragraph.Range.Information($wdActiveEndPageNumber)
                Write-Output ("{0,4}  {1}" -f $page, $text)
            }
        }
    }

    $totalPages = $document.ComputeStatistics($wdStatisticPages, $false)
    Write-Output ("{0,4}  [HET TAI LIEU]" -f $totalPages)

    $document.Close($false)
}
finally {
    $word.Quit()
    [System.Runtime.InteropServices.Marshal]::ReleaseComObject($word) | Out-Null
}
