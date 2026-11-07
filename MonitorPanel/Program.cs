using System;
using System.Diagnostics;
using System.IO;
using System.Windows.Forms;

namespace MCServerPanel
{
    static class Program
    {
        [STAThread]
        static void Main()
        {
            string htmlPath = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "monitor.html");
            if (File.Exists(htmlPath))
            {
                Process.Start(new ProcessStartInfo(htmlPath) { UseShellExecute = true });
            }
            else
            {
                MessageBox.Show("找不到monitor.html文件", "错误", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }
    }
}
