	.file	"bubbleSort.c"
	.text
	.globl	swap
	.type	swap, @function
swap:
.LFB23:
	.cfi_startproc
	movl	(%rdi), %eax
	movl	(%rsi), %edx
	movl	%edx, (%rdi)
	movl	%eax, (%rsi)
	ret
	.cfi_endproc
.LFE23:
	.size	swap, .-swap
	.globl	bubbleSort
	.type	bubbleSort, @function
bubbleSort:
.LFB24:
	.cfi_startproc
	leal	-1(%rsi), %r8d
	testl	%r8d, %r8d
	jle	.L2
	jmp	.L4
.L6:
	movl	(%rax), %edx
	movl	4(%rax), %ecx
	cmpl	%ecx, %edx
	jle	.L5
	movl	%ecx, (%rax)
	movl	%edx, 4(%rax)
.L5:
	addq	$4, %rax
	cmpq	%rsi, %rax
	jne	.L6
.L7:
	subl	$1, %r8d
	je	.L2
.L4:
	testl	%r8d, %r8d
	jle	.L7
	movq	%rdi, %rax
	leal	-1(%r8), %edx
	leaq	4(%rdi,%rdx,4), %rsi
	jmp	.L6
.L2:
	rep ret
	.cfi_endproc
.LFE24:
	.size	bubbleSort, .-bubbleSort
	.globl	fill_array
	.type	fill_array, @function
fill_array:
.LFB25:
	.cfi_startproc
	testl	%esi, %esi
	je	.L10
	movl	$0, %eax
.L11:
	movl	%eax, (%rdi,%rax,4)
	addq	$1, %rax
	cmpq	$100, %rax
	jne	.L11
	rep ret
.L10:
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	pushq	%rbx
	.cfi_def_cfa_offset 24
	.cfi_offset 3, -24
	subq	$8, %rsp
	.cfi_def_cfa_offset 32
	movq	%rdi, %rbx
	leaq	400(%rdi), %rbp
.L13:
	movl	$0, %eax
	call	rand
	movl	%eax, (%rbx)
	addq	$4, %rbx
	cmpq	%rbp, %rbx
	jne	.L13
	addq	$8, %rsp
	.cfi_def_cfa_offset 24
	popq	%rbx
	.cfi_restore 3
	.cfi_def_cfa_offset 16
	popq	%rbp
	.cfi_restore 6
	.cfi_def_cfa_offset 8
	ret
	.cfi_endproc
.LFE25:
	.size	fill_array, .-fill_array
	.globl	main
	.type	main, @function
main:
.LFB26:
	.cfi_startproc
	pushq	%rbx
	.cfi_def_cfa_offset 16
	.cfi_offset 3, -16
	movl	$400, %edi
	call	malloc
	movslq	%eax, %rbx
	movl	$0, %esi
	movq	%rbx, %rdi
	call	fill_array
	movl	$100, %esi
	movq	%rbx, %rdi
	call	bubbleSort
	movl	$0, %eax
	popq	%rbx
	.cfi_def_cfa_offset 8
	ret
	.cfi_endproc
.LFE26:
	.size	main, .-main
	.ident	"GCC: (Ubuntu 5.4.0-6ubuntu1~16.04.10) 5.4.0 20160609"
	.section	.note.GNU-stack,"",@progbits
