using System;
using System.IO;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Security.Cryptography;

namespace InjectSongLengths
{
    public class FileLenInfo
    {
        public string filename;
        public string[] times;
    }

    class Program
    {
        static bool verbose = false;
        static string[] songlengthsfile;
        static Dictionary<string, FileLenInfo> fileLengths = new Dictionary<string,FileLenInfo>();
        static byte[] sidfile;
        static int converted = 0;
        static int skipped = 0;
        static string lasthash;

        static void HandleFile(string filename)
        {
            if (verbose)
            {
                Console.WriteLine("- {0}", filename);
            }
            if (filename.ToLower().Equals(@"songlengths.txt") ||
                filename.ToLower().Equals(@"injectsonglengths.exe"))
            {
                if (verbose)
                {
                    Console.WriteLine("Internal file");
                }
                // skipped++;
                return;
            }
            try
            {
                sidfile = File.ReadAllBytes(filename);
            }
            catch (Exception)
            {
                if (!verbose)
                {
                    Console.WriteLine("- {0}", filename);
                }
                Console.WriteLine("ERROR: Could not open file!");
                // skipped++;
                return;
            }
            if (sidfile.Length < 0x90)
            {
                if (!verbose)
                {
                    Console.WriteLine("- {0}", filename);
                }
                Console.WriteLine("Skipping file ... too small");
                skipped++;
                return;
            }
            if (sidfile[1] != 'S' || sidfile[2] != 'I' || sidfile[3] != 'D')
            {
                if (!verbose)
                {
                    Console.WriteLine("- {0}", filename);
                }
                Console.WriteLine("Skipping file ... not a SID file");
                skipped++;
                return;
            }
            if (sidfile[4] != 0 || sidfile[5] != 2)
            {
                if (!verbose)
                {
                    Console.WriteLine("- {0}", filename);
                }
                Console.WriteLine("Skipping file ... not a version 2 SID file");
                skipped++;
                return;
            }
            // We have a valid v2 SID file here, try to find a match

            FileLenInfo found = FindMD5();

            if (found == null)
            {
                if (!verbose)
                {
                    Console.WriteLine("- {0}", filename);
                }
                Console.WriteLine("{0}SID Hash not found: {1}",(char)sidfile[0], lasthash);
                skipped++;
                return;

            }

            byte selsong = (byte)(sidfile[0x10]*256 + sidfile[0x11] - 1);
            string sstext = found.times[selsong];
            if (sstext.IndexOf(':') == 1)
            {
                sstext = "0" + sstext;
            }
            //            sidfile[0x08] = (byte)sstext[0]; // minutes
            //            sidfile[0x09] = (byte)sstext[1];
            //            sidfile[0x7a] = (byte)sstext[3]; // seconds
            //            sidfile[0x7b] = (byte)sstext[4];

            sidfile[0x7a] = (byte)((((byte)sstext[3] & 0x0f) << 4) | ((byte)sstext[4] & 0x0f)); // seconds
            sidfile[0x7b] = (byte)((((byte)sstext[0] & 0x0f) << 4) | ((byte)sstext[1] & 0x0f)); // minutes

            File.WriteAllBytes(filename, sidfile);

            if (verbose)
            {
                Console.WriteLine("Found MD5 for: {0}  Song: {1}  Time: {2}", found.filename, selsong+1, sstext.Substring(0,5));
            }

            converted++;
        }

        static FileLenInfo FindMD5()
        {
            int i;
            MD5 md5Hash = MD5.Create();

            byte valueVbiSpeed = 0;
            byte valueCiaSpeed = 60;
            byte valueNtscClock = 2;
                
            bool RSID = false;
            if ((char)sidfile[0] == 'R')
            {
                RSID = true;
            }
            int dataoffset = (sidfile[0x06] << 8) + sidfile[0x07];
            int songs = (sidfile[0x0e] << 8) + sidfile[0x0f];
            int datalen = sidfile.Length - (dataoffset + 2);

            int speed = -1;
            if (!RSID)
            {
                speed = (sidfile[0x12] << 24) + (sidfile[0x13] << 16) + (sidfile[0x14] << 8) + (sidfile[0x15]);
            }
            int NTSC = 0;
            bool PlaySIDSpecific = false;

            if (dataoffset >= 0x77)
            {
                if ((sidfile[0x77] & 0x0c) == 0x08)
                {
                    NTSC = 1;
                }
                if (!RSID)
                {
                    if ((sidfile[0x77] & 0x02) > 0)
                    {
                        PlaySIDSpecific = true;
                    }
                }
            }

            byte[] hashmem = new byte[datalen + 6 + songs + NTSC];

            Buffer.BlockCopy(sidfile, dataoffset + 2, hashmem, 0, datalen);
            i = datalen;

            hashmem[i++] = sidfile[0x0b]; // init
            hashmem[i++] = sidfile[0x0a];
            hashmem[i++] = sidfile[0x0d]; // play
            hashmem[i++] = sidfile[0x0c];
            hashmem[i++] = sidfile[0x0f]; // # songs
            hashmem[i++] = sidfile[0x0e];

            for (int j = 0; j < songs; j++)
            {
                bool VbiSpeed = false;
                if (!PlaySIDSpecific)
                {
                    if (j < 31)
                    {
                        if ((speed & (1 << j)) == 0)
                        {
                            VbiSpeed = true;
                        }
                    }
                    else
                    {
                        if ((speed & 0x80000000) == 0)
                        {
                            VbiSpeed = true;
                        }
                    }
                }
                else
                {
                    if ((speed & (01 << (j % 32))) == 0)
                    {
                        VbiSpeed = true;
                    }
                }
                if (RSID)
                {
                    hashmem[i++] = valueCiaSpeed;
                }
                else if (VbiSpeed)
                {
                    hashmem[i++] = valueVbiSpeed;
                }
                else
                {
                    hashmem[i++] = valueCiaSpeed;
                }
            }
            if (NTSC == 1)
            {
                hashmem[i++] = valueNtscClock;
            }

            byte[] hash = md5Hash.ComputeHash(hashmem);
            int size = md5Hash.HashSize;

            StringBuilder sBuilder = new StringBuilder();
            for (i = 0; i < hash.Length; i++)
            {
                sBuilder.Append(hash[i].ToString("x2"));
            }
            string hashstring = sBuilder.ToString();

            lasthash = hashstring;

            if (fileLengths.ContainsKey(hashstring))
            {
                return fileLengths[hashstring];
            }

            return null;
        }

        static void ParseSongLengths()
        {
            int curr = 0;

            FileLenInfo fli = null;

            if (verbose)
            {
                Console.WriteLine("-- Parsing Filelengths.txt file...");
            }

            while (curr < songlengthsfile.Length)
            {
                if (songlengthsfile[curr].Length == 0)
                {
                    curr++;
                    continue;
                }
                if (songlengthsfile[curr][0] == '[')    // Database
                {
                    curr++;
                    continue;
                }
                if (songlengthsfile[curr][0] == ';')    // Comment, filename
                {
                    fli = new FileLenInfo();
                    fli.filename = songlengthsfile[curr].Substring(2);
                }
                else  // MD5 and times
                {
                    string md5 = songlengthsfile[curr].Substring(0, 32);

                    // Get Times
                    string[] sls = songlengthsfile[curr].Substring(33).Split(' ');
                    fli.times = sls;

                    fileLengths.Add(md5, fli);
                }
                curr++;
            }

        }

        static void Main(string[] args)
        {
            if (args.Length > 0)
            {
                if (args[0].ToLower().Equals("-v"))
                {
                    verbose = true;
                }
            }
            try
            {
                songlengthsfile = File.ReadAllLines("Songlengths.txt");
            }
            catch (Exception)
            {
                Console.WriteLine("-- ERROR: Couldn't read Songlenghts.txt file!");
                return;
            }
            ParseSongLengths();
            try
            {
                if (verbose)
                {
                    Console.WriteLine("-- Injecting Times...");
                }
                var files = from file in Directory.EnumerateFiles(@".") select file;

                foreach (var file in files)
                {
                    HandleFile(Path.GetFileName(file));
                }
            }
            catch (UnauthorizedAccessException UAEx)
            {
                Console.WriteLine(UAEx.Message);
            }
            catch (PathTooLongException PathEx)
            {
                Console.WriteLine(PathEx.Message);
            }
            Console.WriteLine("-- Injected {0} files. Skipped {1} files.", converted, skipped);
        }
    }
}
