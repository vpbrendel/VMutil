#!/usr/bin/perl
#
# splitFASTAbyLength.pl
#
# - a script to 

# Usage: splitFASTAbyLength.pl [-h] -m MinimumLength <FASTAfile> > output
#
# Example.
#
# ... 
#     
#

sub print_usage {
  print "\n";
  print "Usage: splitFASTAbyLength.pl [-h] -m MinimumLength <FASTAfile>";
  print "\n\n";
  print "  MinimumLength: required argument";
  print "\n";
  print "  Output: short<FASTAfile> = FASTA file with < MinimumLength entries.";
  print "\n";
  print "          long<FASTAfile> = FASTA file with >= MinimumLength entries.";
  print "\n\n";
}

my $minlgth = -1;

while ((@ARGV > 0) && ($ARGV[0] =~ /^-./)) {
  if ($ARGV[0] eq '-h') {
    print_usage();
    exit;
  } elsif ($ARGV[0] eq '-m') {
    $minlgth = $ARGV[1];
    shift;
    shift;
  } else {
  break;
  }
}

if ($minlgth == -1) {
  print_usage();
  exit;
}

my $fastafile = $ARGV[$ARGV];
my $shortfile = "short" . $fastafile;
my $longfile = "long" . $fastafile;

open(SFILE,">$shortfile");
open(LFILE,">$longfile");

while ($_ = <>) {
  if (/^>/) {
      my $seqname = $_;
      my $seq = "";
NSQ:  while ($_ = <>) {
	if (/^[^>]/) {
	  $seq .= $_;
	}
	else {
          $length = $seq =~ tr/a-zA-Z/a-zA-Z/;
          if ($length >= $minlgth) {
            print LFILE $seqname;
            print LFILE $seq;
          } else {
            print SFILE $seqname;
            print SFILE $seq;
          }
          $seqname = $_;
          $seq = "";
	  next NSQ;
	}
      }
      $length = $seq =~ tr/a-zA-Z/a-zA-Z/;
      if ($length >= $minlgth) {
        print LFILE $seqname;
        print LFILE $seq;
      } else {
        print SFILE $seqname;
        print SFILE $seq;
      }
      print "\nNumber of entries:\n\n";
      my $count = `egrep -c "^>" $fastafile`;
      printf "%40s %6d\n", $fastafile, $count;
      $count = `egrep -c "^>" short$fastafile`;
      printf "%40s %6d\n", "short$fastafile", $count;
      $count = `egrep -c "^>" long$fastafile`;
      printf "%40s %6d\n", "long$fastafile", $count;
      exit;
  }
}
